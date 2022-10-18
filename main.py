import numpy as np
import math
import argparse
import pandas as pd

#from SingleCollisionDCF import arrivalTimeA,arrivalTimeC

from SingleCollisionDCF import SingleCollisionDCF
from SingleCollisionVCS import SingleCollisionVCS
from HiddenTerminalDCF import HiddenTerminalDCF
from HiddenTerminalVCS import HiddenTerminalVCS
from Plot import plot_wrapper
'''
NOTES
Data frame size: 1000 bytes
Slot duration = 10us
BW = 8 Mbps
CW = 4 slots  --> CWmax = 1024
DIFS = 4 slots
SIFS = 1 slot
ACK, RTS, CTS = 2 slots
Lambda = 100, 200, 300, 400, 700, 1000 frames/sec

Total # slots --> 10s / 10u = 1e6


QUESTIONS

'''

def main():
    '''
    main is set up so far for SingleCollision DCF 
    we can put in a separate function later if we want, wasn't sure which separation approach was best
    
    slotdur = 10e-6
    totalSlots = 10 / slotdur 
    frame = 1000 * 8 / 10e-6  #number of slots of frame 1000 bytes
    globalT = 0 # Global timer (in slots)
    transmissionA = 0 # Count for number of transmissions
    transmissionC = 0 # Count for number of transmissions
    CW = 4
    CWmax = 1024
    backoffA = np.random.randint(0, CW-1)
    backoffB = np.random.randint(0, CW-1)

    arrivalA = arrivalTimeA(totalSlots, 100) # totalSlots, lambda
    arrivalC = arrivalTimeC(totalSlots, 100) # totalSlots, lambda

    while (globalT < totalSlots):

        # hard coded process for first index
        # TODO: loop correctly
        if(arrivalA.at(0) > arrivalC.at(0)):
            # Transmit A
            globalT = arrivalA.at(0)
            
            transmissionA+=1

            #if global timer (after transmitting A) is past C's arrival time, transmit C
            if (globalT > arrivalC.at(0)):
                #Transmit C
                transmissionC+= 1

        elif(arrivalC.at(0) > arrivalA.at(0)):
            #Transmit C
            globalT = arrivalC.at(0)
            transmissionC+= 1

            #if global timer (after transmitting C) is past C's arrival time, transmit A
            if (globalT > arrivalA.at(0)):
                #Transmit A
                transmissionA+= 1

       
    

'''

def wrapper(parameters):
    # Frame rates are declared in project outline.
    frameRates = [100,200,300,400,700,1000]
    # frameRates = list(range(200,2010))
    # frameRates = frame_rates[0::10]
    # Loops through each frame rate for analysis.
    columns = ['scenario',
                'FrameRate',
                'NumCollisions',
                'NumASuccesses',
                'NumCSuccesses',
                'AThroughputBits',
                'CThroughputBits',
                'FairnessIndex']
    singleCollisionDCF = list()
    singleCollisionVCS = list()
    hiddenTerminalDCF = list()
    hiddenTerminalVCS = list()
    for FrameRate in frameRates:
        singleCollisionDCF.append(['Single Collision with DCF'] + SingleCollisionDCF(parameters,FrameRate))
        singleCollisionVCS.append(['Single Collision with VCS'] + SingleCollisionVCS(parameters,FrameRate))
        hiddenTerminalDCF.append(['Hidden Terminal with DCF'] + HiddenTerminalDCF(parameters,FrameRate))
        hiddenTerminalVCS.append(['Hidden Terminal with VCS'] + HiddenTerminalVCS(parameters,FrameRate))
    data = singleCollisionDCF + singleCollisionVCS + hiddenTerminalDCF + hiddenTerminalVCS
    data_frame = pd.DataFrame(data=data, columns=columns)
    plot_wrapper(data_frame)

class Parameters():
    def __init__(self):
        description = 'command line inputs'
        parser = argparse.ArgumentParser(description=description)
        # parses command line inputs.
        inputs = self.parseArgs(parser)
        # assigns inputs from parseArgs function to class members
        self.FrameSizeByte = inputs.FrameSizeByte
        self.FrameSize = inputs.FrameSize
        self.ACK = inputs.ACK
        self.SlotDuration_us = inputs.SlotDuration_us
        self.DIFS = inputs.DIFS
        self.SIFS = inputs.SIFS
        self.CW_min = inputs.CW_min
        self.CW_max = inputs.CW_max
        self.MaxTime = inputs.MaxTime
    def parseArgs(self, parser):
        
        parser.add_argument('--FrameSizeByte', dest='FrameSizeByte', type=int,
                            action='store', default=1000,
                            help='Frame size in bytes for network.')
        
        parser.add_argument('--FrameSize', dest='FrameSize', type=int,
                            action='store', default=50,
                            help='Frame size in slots for network.')
        
        parser.add_argument('--ACK', dest='ACK', type=int,
                            action='store', default=2,
                            help='Duration in slots for ACK protocol.')
        
        parser.add_argument('--SlotDuration_us', '-sd', dest='SlotDuration_us', type=int,
                            action='store', default=10e-6,
                            help='Conversion factor for slot duration to sec.')
        
        parser.add_argument('--DIFS', dest='DIFS', type=int,
                            action='store', default=4,
                            help='Duration in slots for DIFS protocol.')
        
        parser.add_argument('--SIFS', dest='SIFS', type=int,
                            action='store', default=1,
                            help='Duration in slots for SIFS protocol.')
        
        parser.add_argument('--CW_min', dest='CW_min', type=int,
                            action='store', default=4,
                            help='Initial transmission window dur in slots.')
        
        parser.add_argument('--CW_max', dest='CW_max', type=int,
                            action='store', default=1024,
                            help='Max transmission window dur in slots.')
        
        parser.add_argument('--max_sim_time', dest='MaxTime', type=int,
                            action='store', default=10,
                            help='Duration for the simulation.')
        
        return parser.parse_args()

if __name__ == "__main__":
    parameters = Parameters()
    wrapper(parameters)
