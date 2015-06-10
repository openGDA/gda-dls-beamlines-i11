'''
Created on 9 Jun 2015

@author: fy65
'''
from peloop.tfg2 import TFG2
from uk.ac.gda.devices.mythen.epics import MythenDetector
from gda.data import NumTracker
from gda.device.scannable import SimpleScannable, ScannableBase

mythen=MythenDetector()
tfg2=TFG2()
scanNumTracker = NumTracker("i11");
delayTime=SimpleScannable()

class TimeResolvedExperimentScannable(ScannableBase):
    def __init__(self, numberOfFrames, numberOfGates, gateTime, delayScannable, tfg, detector, writerTime):
        self.numberOfFrames=numberOfFrames
        self.numberOfGate=numberOfGates
        self.gateTime=gateTime
        self.delayScannable=delayScannable
        self.tfg=tfg
        self.detector=detector
        self.writerTime=writerTime
        
    def atScanStart(self):
        self.collectionNumber = 0;
        self.scanNumber = scanNumTracker.getCurrentFileNumber();

    def atPointStart(self):
        tfg2.configure4TimeResolvedExperiment(self.gateTime, self.numberOfGate, self.numberOfFrames, float(self.delayScannable.getPosition()), self.writerTime)
        mythen.gated(self.numberOfFrames, self.numberOfGate, self.scanNumber , self.collectionNumber)
        
    def getPosition(self):
        return delayTime.getPosition()
    
    def asynchronousMoveTo(self, value):
        tfg2.start()
        
    def isBusy(self):
        return not tfg2.status()=="IDLE"
    
    def stop(self):
        tfg2.stop()
        
    def atPointEnd(self):
        self.collectionNumber++
        
    def atScanEnd(self):
        pass

def doCollection(gatesize, numberofgates, numberofframes, delaybefore, writerTime, detector=mythen, tfg=tfg2):
    
    tfg2.configure4TimeResolvedExperiment(gatesize, numberofgates, numberofframes, delaybefore, writerTime)
    scanNumber=scanNumTracker.incrementNumber()
    mythen.gated(numberofframes, numberofgates, scanNumber, collectionNumber)
