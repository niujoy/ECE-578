
import numpy as np
import math

from Node import Node, State, Channel
from Calculations import calcFairnessIndex, calcThroughputBits

def SingleCollisionVCS(parameters,FrameRate):
    A = Node(parameters, FrameRate, seed=3)
    C = Node(parameters, FrameRate, seed=5)
    channel = Channel(parameters)
    NumCollisions = 0
    NumASuccesses = 0
    NumCSuccesses = 0

    #number of slots for 10 seconds
    MaxSlots = math.ceil(parameters.MaxTime/parameters.SlotDuration_us)
    
    for slot in range(0, MaxSlots):
        #checks if a packet is ready for transmit and adds it to queue
        A.checkState(slot, C)
        C.checkState(slot, A)
        if not channel.is_idle:
            channel.idle_count -= 1
            if channel.idle_count <= 0:
                channel.is_idle = True
                channel.idle_count = parameters.FrameSize + parameters.SIFS + parameters.ACK + 2 + 2 + 1 + 1
                if A.state == State.transmit:
                    A.state = State.idle
                if C.state == State.transmit:
                    C.state = State.idle
            continue
        if A.state == State.readyTransmit:
            if A.backoff is None:
                A. calcBackoff()
            A.state = State.waitTransmit
    
        if C.state == State.readyTransmit:
            if C.backoff is None:
                C. calcBackoff()
            C.state = State.waitTransmit
        
        if A.state == State.waitTransmit:
            #wait until channel is idle for DIFS slots
            if channel.is_idle:
                A.difs_duration -= 1
            else:
                A.difs_duration = 4
            if A.difs_duration <= 0:
                #decrement backoff slots
                if channel.is_idle:
                    A.backoff -= 1
                    if A.backoff <= 0:
                        #send RTS + NAV
                        A.state = State.transmit
        
        if C.state == State.waitTransmit:
            if channel.is_idle:
                C.difs_duration -= 1
            else:
                C.difs_duration = 4
            if C.difs_duration <= 0:
                # decrement backoff slots
                if channel.is_idle:
                    C.backoff -= 1
                    if C.backoff <= 0:
                        #send RTS + NAV
                        C.state = State.transmit
        
        if A.state == State.transmit and C.state == State.transmit:
            #collision
            NumCollisions += 1
            A.cw = A.cw * 2
            A.backoff = None
            A.state = State.idle
            A.difs_duration = 4
            C.cw = C.cw * 2
            C.backoff = None
            C.state = State.idle
            C.difs_duration = 4
        elif A.state == State.transmit and not C.state == State.transmit:
            channel.is_idle = False
            A.backoff = None
            NumASuccesses += 1
            A.cw = A.cw_min
            C.cw = C.cw_min
            A.queue.get()
            A.difs_duration = 4
            C.difs_duration = 4

        elif not A.state == State.transmit and C.state == State.transmit:
            channel.is_idle = False
            C.backoff = None
            NumCSuccesses += 1
            A.cw = A.cw_min
            C.cw = C.cw_min
            C.queue.get()
            A.difs_duration = 4
            C.difs_duration = 4
                   
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

