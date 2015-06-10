'''
This module defines a Scannable class that delivers time resolved experiment data collection. 
It is implemented as a scannable so that it will support easy integration with other sample 
environment scannables, such as laser or temperature controller.

This module delivers 2 scannables for use in GDA 'scan' command
    1. a 'delayTime' scannable - allow scan the delayTime between laser pulse and PSD exposure;
    2. a 'timeresolvedscannable' - which integrate tfg2 and mythen detector to deliver diffraction data at specified delay time.
Usages:
    1. you need to configure 
        >>>timeresolvedscannable.config(numberOfFrames, numberOfGates, gateTime, writerTime )
    2. do data collection with 
        scan delayTime 0.0 1.0 0.01 timeresolvedscannable

Created on 9 Jun 2015

@author: fy65
'''
#from peloop.tfg2 import TFG2
#from uk.ac.gda.devices.mythen.epics import MythenDetector
from gda.data import NumTracker
from gda.device.scannable import SimpleScannable, ScannableBase

#mythen=MythenDetector()
#tfg2=TFG2()
scanNumTracker = NumTracker("i11");
delayTime=SimpleScannable()

class TimeResolvedExperimentScannable(ScannableBase):
    def __init__(self, name, numberOfFrames, numberOfGates, gateTime, writerTime, delayScannable=delayTime, tfg=tfg2, detector=mythen):  # @UndefinedVariable
        self.name=name
        self.numberOfFrames=numberOfFrames
        self.numberOfGate=numberOfGates
        self.gateTime=gateTime
        self.delayScannable=delayScannable
        self.tfg=tfg
        self.detector=detector
        self.writerTime=writerTime
        self.collectionNumber = 0;
        self.scanNumber = scanNumTracker.getCurrentFileNumber()
        self.setLevel(9)
        
    def config(self, numberOfFrames, numberOfGates, gateTime, writerTime ):
        self.setNumberOfFrames(numberOfFrames)
        self.setNumberOfGates(numberOfGates)
        self.setGateTime(gateTime)
        self.setWriterTime(writerTime)
        
    def atScanStart(self):
        self.collectionNumber = 0;
        self.scanNumber = scanNumTracker.getCurrentFileNumber();

    def atPointStart(self):
        self.tfg.configure4TimeResolvedExperiment(self.gateTime, self.numberOfGate, self.numberOfFrames, float(self.delayScannable.getPosition()), self.writerTime)
        self.detector.gated(self.numberOfFrames, self.numberOfGate, self.scanNumber , self.collectionNumber)
        
    def getPosition(self):
        return self.collectionNumber
    
    def asynchronousMoveTo(self, value):
        self.tfg.start()
        
    def isBusy(self):
        return not self.tfg.status()=="IDLE"
    
    def stop(self):
        self.tfg.stop()
        
    def atPointEnd(self):
        self.collectionNumber=self.collectionNumber+1
        
    def atScanEnd(self):
        pass

    def getNumberOfFrames(self):
        return self.numberOfFrames
    def setNumberOfFrames(self,value):
        self.numberOfFrames=value
        
    def getNumberOfGates(self):
        return self.numberOfGate
    def setNumberOfGates(self,value):
        self.numberOfGate=value
        
    def getGateTime(self):
        return self.gateTime
    def setGateTime(self, value):
        self.gateTime=value
        
    def getDelayScannable(self):
        return self.delayScannable
    def setdelayScannable(self, scannable):
        self.delayScannable=scannable
        
    def getTfg(self):
        return self.tfg
    def setTtg(self, tfgObject):
        self.tfg=tfgObject
        
    def getDetector(self):
        return self.detector
    def setDetector(self, detector):
        self.detector=detector
        
    def getWriterTime(self):
        return self.writerTime
    def setWriterTime(self,value):
        self.writerTime=value
        
#example time resolved experiment scannable object
timeresolvedscannable=TimeResolvedExperimentScannable("timeresolvedscannable",1, 10, 0.00001, 2.0, delayScannable=delayTime, tfg=tfg2, detector=mythen)   # @UndefinedVariable

