'''
Created on 15 Feb 2011

@author: fy65
'''
from gda.device.scannable import ScannableMotionBase
from gda.epics import CAClient
from gda.factory import FactoryException
from gov.aps.jca import CAException
import sys

#EPICS PVs
fgfuncpv="BL11I-EA-FGEN-01:FUNC"
fgoutonpv="BL11I-EA-FGEN-01:OUT"
fgfreqpv="BL11I-EA-FGEN-01:FREQ"
fgfreqrbv="BL11I-EA-FGEN-01:FREQ:RBV"
fgamppv="BL11I-EA-FGEN-01:AMP"
fgamprbv="BL11I-EA-FGEN-01:AMP:RBV"
fgoffsetpv="BL11I-EA-FGEN-01:OFF"
fgoffsetrbv="BL11I-EA-FGEN-01:OFF:RBV"
fgsympv="BL11I-EA-FGEN-01:SYMM"
fgsymrbv="BL11I-EA-FGEN-01:SYMM:RBV"

class FunctionGenerator(ScannableMotionBase):
    
    def __init__(self, name, func=fgfuncpv, output=fgoutonpv, freq=fgfreqpv, amp=fgamppv, fgoffset=fgoffsetpv, freqrbv=fgfreqrbv, amprbv=fgamprbv,offsetrbv=fgoffsetrbv, symmetry=fgsympv, symmetryrbv=fgsymrbv):
        self.setName(name)
        self.setInputNames(["frequency","amplitude","shift","symmetry"])
        self.setExtraNames([])
        self.function=CAClient(func)
        self.output=CAClient(output)
        self.frequency=CAClient(freq)
        self.frequencyrbv=CAClient(freqrbv)
        self.amplitude=CAClient(amp)
        self.amplituderbv=CAClient(amprbv)
        self.shiftcli=CAClient(fgoffset)
        self.shiftrbv=CAClient(offsetrbv)
        self.symmetry=CAClient(symmetry)
        self.symmetryrbv=CAClient(symmetryrbv)
    
    # function generator controls
    def setFunction(self, function):
        try:
            if not self.function.isConfigured():
                self.function.configure()
            self.function.caput(function)
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.function.getChannel().getName(),e)
        except CAException, e:
            print "caput Error (%s): %s" % (self.function.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def getFunction(self):
        try:
            if not self.function.isConfigured():
                self.function.configure()
            return float(self.function.caget())
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.function.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.function.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def setOutput(self, output):
        try:
            if not self.output.isConfigured():
                self.output.configure()
            self.output.caput(output)
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.output.getChannel().getName(),e)
        except CAException, e:
            print "caput Error (%s): %s" % (self.output.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def getOutput(self):
        try:
            if not self.output.isConfigured():
                self.output.configure()
            return float(self.output.caget())
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.output.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.output.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def setFrequency(self, frequency):
        try:
            if not self.frequency.isConfigured():
                self.frequency.configure()
            self.frequency.caput(frequency)
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.frequency.getChannel().getName(),e)
        except CAException, e:
            print "caput Error (%s): %s" % (self.frequency.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def getFrequency(self):
        try:
            if not self.frequencyrbv.isConfigured():
                self.frequencyrbv.configure()
            return float(self.frequencyrbv.caget())
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.frequencyrbv.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.frequencyrbv.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def setAmplitude(self, amplitude):
        try:
            if not self.amplitude.isConfigured():
                self.amplitude.configure()
            self.amplitude.caput(amplitude)
        except FactoryException, e:
            print "create channel error: %s" % (self.amplitude.getChannel().getName(),e)
        except CAException, e:
            print "caput Error (%s): %s" % (self.amplitude.getChannel().getName(),e)
        except:
            print "Unexpected error (%s):", sys.exc_info()[0]
            raise

    def getAmplitude(self):
        try:
            if not self.amplituderbv.isConfigured():
                self.amplituderbv.configure()
            return float(self.amplituderbv.caget())
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.amplituderbv.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.amplituderbv.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        
    def setShift(self, amplitude):
        try:
            if not self.shiftcli.isConfigured():
                self.shiftcli.configure()
            self.shiftcli.caput(amplitude)
        except FactoryException, e:
            print "create channel error: %s" % (self.shiftcli.getChannel().getName(),e)
        except CAException, e:
            print "caput Error (%s): %s" % (self.shiftcli.getChannel().getName(),e)
        except:
            print "Unexpected error (%s):", sys.exc_info()[0]
            raise

    def getShift(self):
        try:
            if not self.shiftrbv.isConfigured():
                self.shiftrbv.configure()
            return float(self.shiftrbv.caget())
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.shiftrbv.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.shiftrbv.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

       
    def setSymmetry(self, value):
        try:
            if not self.symmetry.isConfigured():
                self.symmetry.configure()
            self.symmetry.caput(value)
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.symmetry.getChannel().getName(),e)
        except CAException, e:
            print "caput Error (%s): %s" % (self.symmetry.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def getSymmetry(self):
        try:
            if not self.symmetryrbv.isConfigured():
                self.symmetryrbv.configure()
            return float(self.symmetryrbv.caget())
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.symmetryrbv.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.symmetryrbv.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def getTargetPosition(self):
        freq=0.0
        ampl=0.0
        off=0.0
        sym=0.0
        try:
            if not self.frequency.isConfigured():
                self.frequency.configure()
            freq=float(self.frequency.caget())
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.frequency.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.frequency.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        try:
            if not self.amplitude.isConfigured():
                self.amplitude.configure()
            ampl=float(self.amplitude.caget())
        except FactoryException, e:
            print "create channel error: %s" % (self.amplitude.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.amplitude.getChannel().getName(),e)
        except:
            print "Unexpected error (%s):", sys.exc_info()[0]
            raise
        try:
            if not self.shiftcli.isConfigured():
                self.shiftcli.configure()
            off=float(self.shiftcli.caget())
        except FactoryException, e:
            print "create channel error: %s" % (self.shiftcli.getChannel().getName(),e)
        except CAException, e:
            print "caput Error (%s): %s" % (self.shiftcli.getChannel().getName(),e)
        except:
            print "Unexpected error (%s):", sys.exc_info()[0]
            raise
        try:
            if not self.symmetry.isConfigured():
                self.symmetry.configure()
            sym=float(self.symmetry.caget())
        except FactoryException, e:
            print "create channel error (%s): %s" % (self.symmetry.getChannel().getName(),e)
        except CAException, e:
            print "caget Error (%s): %s" % (self.symmetry.getChannel().getName(),e)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        return freq,ampl,off,sym

    def atScanStart(self):
        '''switch on output'''
        self.setOutput(1) 
    
    def atScanEnd(self):
        '''switch off output'''
        self.setOutput(0)
    
    def getPosition(self):
        try:
            return self.getFrequency(),self.getAmplitude(), self.getShift(),self.getSymmetry()
        except:
            print "failed to get tuple data: ", sys.exc_info()[0]
            raise

    def asynchronousMoveTo(self,new_position):
        try:
            self.setFrequency(new_position[0])
            self.setAmplitude(new_position[1])
            self.setShift(new_position[2])
            self.setSymmetry(new_position[3])
        except:
            print "error moving shiftcli to position (%s): %f" % (sys.exc_info()[0], new_position)
            raise

    def isBusy(self):
        return (self.getPosition() != self.getTargetPosition())

#    def toString(self):
#        return self.name + " : (" + str(self.getPosition()[0]), str(self.getPosition()[1]), str(self.getPosition()[2]), str(self.getPosition()[3])+")"
    
fg=FunctionGenerator("fg")
