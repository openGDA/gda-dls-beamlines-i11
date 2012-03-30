'''
Created on 15 Feb 2011

@author: fy65
'''
from gda.device.scannable import ScannableMotionBase
from gda.epics import CAClient
from gda.factory import FactoryException
from gov.aps.jca import CAException
import sys
from gov.aps.jca.event import MonitorListener
from gda.analysis import Plotter

def sum_datasets(datasets):
    #{0: [1,2,3], 1: [3,4,5], 2: [6,7,8]}
    lists = [x.tolist() for x in datasets.values()]
    if len(lists) == 1:
        return lists[0]
    data = zip(*tuple(lists))
    #[(1,3,6), (2,4,7)...]
    data = [float(sum(xs)) / len(xs) for xs in data]
    #[3.333, ...]
    return data

#EPICS PVs
adcppv="BL11I-EA-PE-01:HV"
adcepv="BL11I-EA-PE-01:EL"

class ADC(ScannableMotionBase, MonitorListener):
    
    def __init__(self, name, hv=adcppv, el=adcepv):
        self.setName(name)
        self.setInputNames([])
        self.voltagecli=CAClient(hv)
        self.electrometercli=CAClient(el)
        self.voltagenordcli=CAClient(hv+".NORD")
        self.electrometernordcli=CAClient(el+".NORD")
        self.monitoradded=False
        self.counter=0
        self.numberofgates=0
        self.numberofframes=0
        self.filename=None
        self.filenames=[]
        self.repetition=0 #0 means no repetition
        self.monitor=None
        self.firstMonitor = True
        self.voltages = {}
        self.electrometers={}
        self.voltage=[]
        self.electrometer=[]
       
    def resetCounter(self):
        self.counter=0
        
    def resetRepetition(self):
        self.repetition=0
        
    def setRepetition(self, num):
        self.repetition=num
        
    def setNumberOfGates(self, num):
        self.numberofgates=num
        
    def setNumberOfFrames(self, num):
        self.numberofframes=num
        
    def getNumberOfGates(self):
        return self.numberofgates
    
    def getNumberOfFrames(self):
        return self.numberofframes
    
    def setFilename(self, filename):
        self.filename=filename
        
    def getFilename(self):
        return self.filename
    
    def getFilenames(self):
        return self.filenames

    def getElectrometer(self, num):
        try:
            if not self.electrometercli.isConfigured():
                self.electrometercli.configure()
            return self.electrometercli.cagetArrayDouble(num)
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.electrometercli.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.electrometercli.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def getVoltage(self, num):
        try:
            if not self.voltagecli.isConfigured():
                self.voltagecli.configure()
            return self.voltagecli.cagetArrayDouble(num)
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.voltagecli.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.voltagecli.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        
    def getElectrometerNord(self):
        try:
            if not self.electrometernordcli.isConfigured():
                self.electrometernordcli.configure()
            return int(float(self.electrometernordcli.caget()))
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.electrometernordcli.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.electrometernordcli.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def getVoltageNord(self):
        try:
            if not self.voltagenordcli.isConfigured():
                self.voltagenordcli.configure()
            return int(float(self.voltagenordcli.caget()))
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.voltagenordcli.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.voltagenordcli.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
   
    def addMonitor(self, count):
        if self.monitoradded:
            #monitor already added, prevent adding more than one monitor
            return
        self.firstMonitor=True
        try:
            if not self.voltagecli.isConfigured():
                self.voltagecli.configure()
            self.monitor=self.voltagecli.camonitor(self, count)
            self.monitoradded=True
        except CAException, e:
            self.monitoradded=False
            print "camonitor Error (%s): %s" % (self.voltagecli.getChannel().getName(),e)
        except:
            self.monitoradded=False
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def removeMonitor(self):
        if not self.monitoradded:
            #monitor does not exist
            return
        self.firstMonitor=True
        try:
            if not self.voltagecli.isConfigured():
                self.voltagecli.configure()
            if self.monitor != None:
                self.pvcli.removeMonitor(self.monitor)
            self.monitoradded=False
        except CAException, e:
            self.monitoradded=True
            print "camonitor Error (%s): %s" % (self.pvcli.getChannel().getName(),e)
        except:
            self.monitoradded=True
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def monitorChanged(self, mevent):
        if self.firstMonitor:
            self.firstMonitor = False
            return        
        if self.counter < self.numberofgates:
            if self.counter not in self.voltages:
                self.voltages[self.counter]=[]
            if self.counter not in self.electrometers:
                self.electrometers[self.counter]=[]
            vnord=self.getVoltageNord()
            enord=self.getElectrometerNord()
            print vnord, enord
            self.voltages[self.counter] = self.getVoltage(vnord)[1:]
            self.electrometers[self.counter] = self.getElectrometer(vnord)[1:]
            #print dir(voltages[self.counter])
            #print len(voltages[self.counter])
            #print type(voltages[self.counter]) #[1:nord]
            #print self.voltages[self.counter][:5]
            self.counter += 1
        if self.counter == self.numberofgates:
            self.filenames.append(self.filename+"_"+self.getName()+"_"+str(self.repetition))
            #kick off a thread to process and save data so not to block monitor event process here.
            #savedata=SaveData(name=self.getName()+"-"+str(self.repetition), args=(self.filenames[self.repetition]+".dat", "w", self.getName()), kwargs=voltages)
            #savedata.start()
            self.save(args=(self.filenames[self.repetition]+".dat", "w", self.getName()), voltages=self.voltages, electrometers=self.electrometers)
            self.voltages={}
            self.electrometers={}
            self.repetition+=1
            self.resetCounter()
            self.filenames=[]
            
    def save(self, args=(), voltages={}, electrometers={}):
        print "summing data points to produce P-E data..."
        self.voltage = sum_datasets(voltages)
        self.electrometer = sum_datasets(electrometers)
        print "plotting PE-loop..."
        if self.firstData:
            Plotter.plot("DataPlot", self.voltage, self.electrometer)
        else:
            Plotter.plotOver("DataPlot", self.voltage, self.electrometer)
        print "%s: saving data to %s" % (args[2], args[0])
        self.file=open(args[0], args[1])
        for voltage, electrometer in self.voltage, self.electrometer:
            self.file.write("%s\t%s\n"%(voltage, electrometer))
        self.file.close()
        print "%s: save data to %s completed." % (args[2], args[0])

    def getExtraNames(self):
        repetition=[]
        for i in range(self.repetition):
            repetition.append(str(i))
        return repetition
    
    def atScanStart(self):
        self.resetCounter()
        self.resetRepetition()
 
    def atScanEnd(self):
        pass

    def atPointStart(self):
        self.resetCounter()
        self.resetRepetition()
    
    def atPointEnd(self):
        pass

    def rawGetPosition(self):
        return self.getFilenames()

    def rawAsynchronousMoveTo(self,new_position):
        pass
    
    def rawIsBusy(self):
        return False
    
#    def toString(self):
#        return self.name + " : " + str(self.getPosition())
adc=ADC("adc")