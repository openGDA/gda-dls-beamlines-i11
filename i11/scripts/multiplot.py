from gda.data import PathConstructor
import os
from plot import plotover, PSD, plot, MAC, SRS
def plots(startNumber, endNumber, commonSuffix="mythen_summed.dat", dataType=PSD):
    firstPlot=True
    datadir=PathConstructor.createFromDefaultProperty()
    for filenumber in range(startNumber, endNumber+1):
        filename=str(filenumber)+"-"+commonSuffix
        if firstPlot:
            plot(dataType, os.path.join(datadir,filename))
            firstPlot=False
        else:
            plotover(dataType, os.path.join(datadir,filename))