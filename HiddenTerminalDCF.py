import numpy as np
import math

from Node import Node, State, Channel
from Calculations import calcFairnessIndex, calcThroughputBits

        
def HiddenTerminalDCF(parameters, FrameRate):
    A = Node(parameters, FrameRate, seed=3)
    C = Node(parameters, FrameRate, seed=5)
    channel = Channel(parameters)
    NumCollisions = 0
    NumASuccesses = 0
    NumCSuccesses = 0

    #number of slots for 10 seconds
    MaxSlots = math.ceil(parameters.MaxTime/parameters.SlotDuration_us)
    
    for slot in range(0, MaxSlots):
        A.checkState(slot, C)
        C.checkState(slot, A)

        if A.state == State.readyTransmit:
            if A.backoff is None:
                A.calcBackoff()
            A.state = State.waitTransmit

        if C.state == State.readyTransmit:
            if C.backoff is None:
                C.calcBackoff()
            C.state = State.waitTransmit
        
        if A.state == State.waitTransmit:
            # DIFS is always decremented because A cannot see C so it always 
            # beleives channel is idle
            A.difs_duration -= 1
            if A.difs_duration <= 0:
                A.backoff -= 1
                if A.backoff <= 0:
                    A.state = State.transmit
                    A.transmit_count = A.calcTransmit(parameters)

        if C.state == State.waitTransmit:
            # DIFS is always decremented because A cannot see C so it always
            # beleives channel is idle
            C.difs_duration -= 1
            if C.difs_duration <= 0:
                C.backoff -= 1
                if C.backoff <= 0:
                    C.state = State.transmit
                    C.transmit_count = C.calcTransmit(parameters)
                    

        if A.state == State.transmit and C.state == State.transmit:
            if A.valid or C.valid:
                A.valid = False 
                C.valid = False
                NumCollisions += 1

        if A.state == State.transmit:
            A.transmit_count -= 1
            if A.transmit_count <= 0:
                if A.valid:
                   NumASuccesses += 1
                   A.queue.get()
                   A.reset()
                else:
                    A.collision()
                   
        if C.state == State.transmit:
            C.transmit_count -= 1
            if C.transmit_count <= 0:
                if C.valid:
                    NumCSuccesses += 1
                    C.queue.get()
                    C.reset()
                else:
                    C.collision()
                   
    AThroughputBits = calcThroughputBits(NumASuccesses,
                                    parameters.FrameSizeByte,
                                    parameters.MaxTime,
                                    scale=10e3)
    CThroughputBits = calcThroughputBits(NumCSuccesses,
                                    parameters.FrameSizeByte,
                                    parameters.MaxTime,
                                    scale=10e3)
    
    FairnessIndex = calcFairnessIndex(NumASuccesses,NumCSuccesses,MaxSlots,parameters)
    return [FrameRate, NumCollisions, NumASuccesses, NumCSuccesses, AThroughputBits, CThroughputBits, FairnessIndex]          

