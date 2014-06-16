'''
a scannable for controlling the gas injection rig system which are used to prepare the sample environment:
    1. Before starting the environment, you must initialise the system using gasrig.initialise();
    2. Then you need to set the system pressure by selecting a mass flow controller, its flow, and target pressure using gdarig.gasin(mcf2,1.0,1.0);
    3. scan the sample pressure,
    4. on completion, vent the system by calling gasrig.complete(). 

Created on 6 Dec 2013
updated on 16 June 2014

@author: fy65
'''
from gasrig.i11gasrig import mfc1, bpr, ventvalve, sampleP, dvpc
#ROOT_PV="BL11I-EA-GIR-01:"
SEQUENCE_CONTROL="SEQ:CON"
SEQUENCE_STATUS="SEQ:STA"
#AT_PRESSURE_PROC="ATPRESSURE.PROC"

sequence={0:"on",1:"off",2:"reset"}

from gda.epics import CAClient 
from gda.device.scannable import ScannableMotionBase

class GasRigClass(ScannableMotionBase):
    '''Create a scannable for a gas injection rig'''
    def __init__(self, name, rootPV):
        self.setName(name);
        self.setInputNames([name])
        self.setLevel(5)
        self.setsequencecli=CAClient(rootPV+SEQUENCE_CONTROL)
        self.statecli=CAClient(rootPV+SEQUENCE_STATUS)
        
    def initialise(self, systemPressure=bpr, samplePressure=dvpc):
        systemPressure.setMode(0)
        samplePressure.setMode(0)
        
    def gasin(self, mfc=mfc1, flow=1.0, pressuretarget=1.0, systemPressure=bpr):
        '''select gas flow control and set system pressure'''
        mfc.asynchronousMoveTo(flow)
        systemPressure.moveTo(pressuretarget)
        mfc.asynchronousMoveTo(0)
        
    def complete(self,valve=ventvalve,systemPressure=bpr, samplePressure=sampleP):
        self.off()
        valve.on()
        systemPressure.asynchronousMoveTo(0)
        samplePressure.asynchronousMoveTo(0)

    def getState(self):
        try:
            if not self.statecli.isConfigured():
                self.statecli.configure()
                output=int(self.statecli.caget())
                self.statecli.clearup()
            else:
                output=int(self.statecli.caget())
            return sequence[output]
        except:
            print "Error returning current state"
            return 0

    def setSequence(self,new_position):
        try:
            if not self.setsequencecli.isConfigured():
                self.setsequencecli.configure()
                self.setsequencecli.caput(new_position)
                self.setsequencecli.clearup()
            else:
                self.setsequencecli.caput(new_position)
        except:
            print "error setting sequence"
            
    def on(self):
        self.setSequence(0)
        
    def off(self):
        self.setSequence(1)
        
    def reset(self):
        self.setSequence(2)
        
#### methods for scannable 
    def getPosition(self):
        return self.getState()
    
    def asynchronousMoveTo(self, new_position):
        self.setSequence(float(new_position))

    def isBusy(self):
        return False

    def atScanStart(self):
        pass
    def atPointStart(self):
        pass
    def stop(self):
        pass
    def atPointEnd(self):
        pass
    def atScanEnd(self):
        pass
    