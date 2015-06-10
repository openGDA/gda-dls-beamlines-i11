'''
Created on 9 Jun 2015

@author: fy65
'''

FORCE_PV="BL11I-EA-SPUMP-01:FORCE"
TARGET_TIME_PV="BL11I-EA-SPUMP-01:TTIME"
DIAMETER_PV="BL11I-EA-SPUMP-01:DIAMETER"
INFUSE_RATE_PV="BL11I-EA-SPUMP-01:IRATE"
WITHDRAW_RATE_PV="BL11I-EA-SPUMP-01:WRATE"

class HASyringePump(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        