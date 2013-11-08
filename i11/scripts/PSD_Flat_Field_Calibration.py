'''
Created on 25 Jul 2012
Usage:
    >>>flatfieldcalibration("20121001", numberofscan, quick[True|False], beamenergy, threshold)
@author: fy65
'''
import os
from gda.configuration.properties import LocalProperties
import datetime
from localStation import getSubdirectory, setSubdirectory

START_ANGLE               = -15
#START_ANGLE               = -18
STOP_ANGLE                = 80

flat_field_delta_velocity = 0.11
#flat_field_delta_velocity = 0.055
standard_delta_velocity   = 1.8

#quick_psd_time            = 68
quick_psd_time            = abs(STOP_ANGLE-START_ANGLE)/standard_delta_velocity+10

#slow_psd_time             = 930
slow_psd_time             = abs(STOP_ANGLE-START_ANGLE)/flat_field_delta_velocity+30
#slow_psd_time             = 1830

SLOW=0
FAST=1

#delta=ScannableMotor()
#from localStation import mythen,smythen
from time import sleep
from plot import plot,RAW

#PSDDIRECTORY="/dls/i11/data/2012/cm5705-4/PSD/"
PSD_FLATFIELD_DIR="/dls/i11/software/mython/diamond/flatfield"
PSD_CALIBRATION_DIR="/dls/i11/software/mython/diamond/calibration"
CURRENT_FLAT_FIELD_FILE="/dls/i11/software/mython/diamond/flatfield/current_flat_field_file"
BAD_CHANNEL_LIST=PSD_CALIBRATION_DIR+os.sep+"badchannel_detector_standard.lst"

def read_raw_data(filename):
    ''' Reads the lines from the specified Mythen raw data file, 
    and returns an array of (channel, count) tuples'''
    f=open(filename,"rb")
    lines=f.readlines()
    f.close()
    return [tuple(map(int, l.strip().split(" "))) for l in lines]


def applyFlatFieldCalibration(sum_flat_field_file):
    os.unlink(CURRENT_FLAT_FIELD_FILE)
    os.symlink(sum_flat_field_file, CURRENT_FLAT_FIELD_FILE)
    print "Current Flat Field data file is update to " + os.readlink(CURRENT_FLAT_FIELD_FILE)
    print "You now need to run 'reset_namespace' for this to take effect! "
    print "IMPORTANT: You must reset delta limits, theta position, and backstop now!!!"


def sumScanRawData(numberofscan, beamenergy, detector=smythen): #@UndefinedVariable
    filenames = []
    for i in range(numberofscan):
        filenames.append(detector.getDataDirectory() + os.sep + detector.buildRawFilename(i))
    
    now = datetime.datetime.now()
    sum_flat_field_file = PSD_FLATFIELD_DIR + os.sep + "Sum_Flat_Field_E" + str(beamenergy) + "keV_T" + str(beamenergy/2) + "eV" + now.strftime("%Y%m%d)") + ".raw"
    summedfile = open(sum_flat_field_file, "w")
    data = map(read_raw_data, filenames)
    for channel in range(len(data[0])):
        values = [data[i][channel][1] for i in range(len(data))]
        summedfile.write("%d %d\n" % (channel, sum(values)))
    
    summedfile.flush()
    summedfile.close()
    print "Summation completed: Flat Field Calibration file is " + sum_flat_field_file
    return sum_flat_field_file


def scanFlatField(numberofscan, detector, motor):
    #motor.moveTo(START_ANGLE) #move to start pangle first before collection
    scancounter=0
    detector.atScanStart() #to initialise collection number and scan number in GDA mythen object
    while scancounter < numberofscan:
        if (scancounter % 2 == 0):
            print "moving delta to " + str(STOP_ANGLE)
            motor.asynchronousMoveTo(STOP_ANGLE)
        else:
            print "move delta to " + str(START_ANGLE)
            motor.asynchronousMoveTo(START_ANGLE)
        detector.collectData()
        sleep(1) #must give time for detector for detector to respond to request.
        while detector.isBusy():
            sleep(0.1)
        
        detector.atPointEnd()
        scancounter += 1
    
    detector.atScanEnd()
    print "flatfield scans completed."

def flatfieldcalibration(filedir, numberofscan, quick, beamenergy, mythenDet=mythen,deltaMotor=delta): #@UndefinedVariable
    defaultdatadir=None
    defaultsubdir=None
    try:
        #1st cache the current data directory and subdirectory metadata
        defaultdatadir=LocalProperties.get("gda.data.scan.datawriter.datadir")
        defaultsubdir=getSubdirectory()
        #create a new directory to store flat field calibration data if not yet exist
        setSubdirectory("PSD")
        setSubdirectory("PSD/"+filedir)
    
        print "moving delta motor to start angle: " + str(START_ANGLE) +" Please wait..."
        deltaMotor.moveTo(START_ANGLE)
        print "delta motor is now at start angle: "+str(deltaMotor.getPosition())
        if quick==FAST:
            print "starting quick scan for "+str(quick_psd_time*numberofscan) +" seconds..."
            deltaMotor.setSpeed(standard_delta_velocity)
            mythenDet.setCollectionTime(quick_psd_time)
            scanFlatField(numberofscan, mythenDet, deltaMotor)
            print "Quick scan completed."
        elif quick==SLOW:
            print "starting flatfield scans for "+str(slow_psd_time*numberofscan) +" seconds..."
            deltaMotor.setSpeed(flat_field_delta_velocity)
            mythenDet.setCollectionTime(slow_psd_time)
            scanFlatField(numberofscan, mythenDet, deltaMotor)
            
            print "Sum all scanned raw data into one flat field data file..."
            sum_flat_field_file = sumScanRawData(numberofscan, beamenergy)
            #plot and view flat field raw data
            plot(RAW,sum_flat_field_file)
            print "Please check the flat field file for any dead pixels, etc.and check that all the bad channels are in the bed channel list at "+BAD_CHANNEL_LIST
            #apply this flat field correction to PSD in GDA permenantly
            applyFlatFieldCalibration(sum_flat_field_file)
        else:
            print "The 3rd input must either SLOW or FAST in upper case."
    except:
        print "exception ocuurred, abort"
    finally:
        if defaultsubdir is not None:
            setSubdirectory(defaultsubdir)
        if defaultdatadir is not None:
            LocalProperties.set("gda.data.scan.datawriter.datadir", defaultdatadir)
    
    
    
    
    