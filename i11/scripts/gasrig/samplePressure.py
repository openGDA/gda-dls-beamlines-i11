'''
a specific scannable for sample pressure control to support gradual gas pressure increments in sample.

Created on 13 Jun 2014

@author: fy65
'''
from gov.aps.jca.event import MonitorListener
from gda.device.scannable import ScannableBase
from time import sleep
import sys
from gda.epics import CAClient
import thread

CurrentPressure = "BL11I-EA-GIR-01:DVPC:P:RD"
TargetPressure = "BL11I-EA-GIR-01:DVPC:SETPOINT:WR"
PressureControl = "BL11I-EA-GIR-01:DVPC:MODE:WR"

class SamplePressure(ScannableBase, MonitorListener):
    '''
    create a sannable to provide control of gas pressure in the sample. 
    It will reports to users when the system pressure is less than the sample pressure requested. 
    '''

    def __init__(self, name, systempressure):
        '''
        Constructor
        '''
        self.setName(name)
        self.setInputNames([name])
        self.increment = 0.01
        self.target = 0.0
        self.sampleP = 0.0
        self.currentpressure = 0.0
        self.pressureTolerance = 0.002
        self.outcli=CAClient(CurrentPressure)
        self.incli=CAClient(TargetPressure)
        self.sysp=systempressure
        
    def atScanStart(self):
        '''intialise parameters before scan'''
        if not self.outcli.isConfigured():
            self.outcli.configure()
        if not self.incli.isConfigured():
            self.incli.configure()
        self.target = self.getPosition()
    
    def atScanEnd(self):
        '''clean up resources'''
        if self.outcli.isConfigured():
            self.outcli.clearup()
        if self.incli.isConfigured():
            self.incli.clearup()
        
    def atPointStart(self):
        pass
    
    def atPointEnd(self):
        pass
        
    def getPosition(self):
        '''
        return the current gas pressure in sample
        '''
        try:
            if not self.outcli.isConfigured():
                self.outcli.configure()
                output=float(self.outcli.caget())
                self.outcli.clearup()
            else:
                output=float(self.outcli.caget())
            return output
        except:
            print "Error returning current position"
            return 0

    def asynchronousMoveTo(self, new_position):
        '''
        move the sample pressure to the specified value asynchronously.
        '''
        try:
            self.sampleP = self.getPosition()
            self.target = float(new_position)
            thread.start_new_thread(self.setSamplePressure, (self.sampleP, self.target, self.increment))
        except:
            print "error moving sample pressure to (%s): %f" % (sys.exc_info()[0], float(new_position))
            raise

    def isBusy(self):
        return (abs(self.getPosition() - self.getTarget())>self.getTolerance())
    
    def stop(self):
        '''
        stop or abort pressure move in the sample.
        '''
        self.asynchronousMoveTo(self.getPosition())
        if self.outcli.isConfigured():
            self.outcli.clearup()
        if self.incli.isConfigured():
            self.incli.clearup()
        
    def setSamplePressure(self, SampleP, target, increment):
        # SET FINAL SAMPLE PRESSURE AND INCREMENTS
        if SampleP<target:
            while SampleP < target:  # final sample pressure in bar
                SampleP += increment  # increments in bar
                try:
                    if not self.incli.isConfigured():
                        self.incli.configure()
                        self.incli.caput(SampleP)
                        self.incli.clearup()
                    else:
                        self.incli.caput(SampleP)
                except:
                    print "error moving to position"
                sleep(5)  # wait time in seconds
                #check if smaple pressure required greater the system pressure then exit
                if self.sysp.getPosition()<target:
                    #TODOs recharge the system pressure here???
                    print "System pressure %f is less than the demanding sample pressure %f. Please abort this scan or re-charge the system pressure." % (self.sysp.getPosition(),target)

        elif SampleP>target:
            while SampleP > target:  # final sample pressure in bar
                SampleP -= increment  # increments in bar
                try:
                    if not self.incli.isConfigured():
                        self.incli.configure()
                        self.incli.caput(SampleP)
                        self.incli.clearup()
                    else:
                        self.incli.caput(SampleP)
                except:
                    print "error moving to position"
                sleep(5)  # wait time in seconds
        else:
            print "already at the sample pressure."
            return
            

    def setIncrement(self, value):
        self.increment = value
        
    def getIncrement(self):
        return self.increment 

    def getTarget(self):
        return self.target
    def initialiseTarget(self):
        self.target=self.getPosition()
    def getTolerance(self):
        return self.pressureTolerance
    def setTolerance(self, value):
        self.pressureTolerance = value


