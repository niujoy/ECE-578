import numpy as np
import math
import numpy as np
import math

from Node import Node, State, Channel
from Calculations import calcFairnessIndex, calcThroughputBits


'''

class SingleDomain:
    def __init__(self, DIFS, SIFS, backoff1, backoff2, ACK, frame):
        self.DIFS = 4
        self.SIFS = 1
        self.ACK = 2
        self.frame = 1000 * 8 / 10e-6  #number of slots of frame 1000 bytes
        # outputs: throughput, rate

def arrivalTimeA(totalSlots, L): # pass in lambda

    set values drawn from poission distribution (Ua, Uc)
    Translate Ua,Uc to exponential values (Xa, Xc)
        Xa = -(1/lambda) * ln(1-Ua)
    Translate Xa,Xc (which are in seconds) to slots
        **Round up to the nearest slot
        Divide each value by slot duration (10us)
    
    arrivalA_P = [] #poisson
    arrivalA_sec = [] #seconds
    arrivalA_S = [] #slots

    while (np.sum(arrivalA_S) < totalSlots): 
        arrivalA_P.append(np.random.random())  
        arrivalA_sec = [(-1/L * math.log(1 - x)) for x in arrivalA_P] 
        arrivalA_S = [(math.ceil(y / 10e-6)) for y in arrivalA_sec] 

    arrivalA_S = np.cumsum(arrivalA_S)

    return arrivalA_S
    
def arrivalTimeC(totalSlots, L): 

    arrivalC_P = []  #poisson
    arrivalC_sec = [] #seconds
    arrivalC_S = [] #slots

    while (np.sum(arrivalC_S) < totalSlots): 
        arrivalC_P.append(np.random.random()) 
        arrivalC_sec = [(-1/L * math.log(1 - x)) for x in arrivalC_P] 
        arrivalC_S = [(math.ceil(y / 10e-6)) for y in arrivalC_sec] 

    arrivalC_S = np.cumsum(arrivalC_S)

    return [arrivalC_S]

def SingleCollisionDCF():
    SCD = SingleDomain
    slotdur = 10e-6
    totalSlots = 10 / slotdur 
    globalT = 0 # Global timer (in slots)
    transmissionA = 0 # Count for number of transmissions
    transmissionC = 0 # Count for number of transmissions
    CW = 4
    CWmax = 1024

    arrivalA = arrivalTimeA(totalSlots, 100) # totalSlots, lambda
    arrivalC = arrivalTimeC(totalSlots, 100) # totalSlots, lambda

    while (globalT < totalSlots):

        backoffA = np.random.randint(0, CW-1)
        backoffC = np.random.randint(0, CW-1)
        # hard coded process for first index
        # TODO: loop correctly

        for i in arrivalA & arrivalC:

            #if collision
            if (arrivalA.at(i) + SCD.DIFS + backoffA == arrivalC.at(i) + SCD.DIFS + backoffC):
                if CW < CWmax:
                    CW = 2 * CW
            else:
                CW = 4

            #if A 
            if (arrivalA.at(i) > arrivalC.at(i)):

                transmissionA+=1

            #if C
            elif (arrivalC.at(i) > arrivalA.at(i)):

                transmissionC+=1

            #if arrival times are equal
            else:

                if backoffA > backoffC:
                    transmissionA+=1

                elif backoffC > backoffA:
                    transmissionC+=1

                else:
                    if CW < CWmax:
                        CW = 2 * CW



        if (arrivalA.at(0) == arrivalC.at(0)):
                #collision
                if (CW < CWmax):
                    CW = 2 * CW

        elif(arrivalA.at(0) > arrivalC.at(0)): #if A
            # Transmit A
            globalT = arrivalA.at(0)
            globalT = globalT + SCD.DIFS + backoffA + SCD.frame + SCD.SIFS + SCD.ACK 
            transmissionA+=1

            #if global timer (after transmitting A) is past C's arrival time, transmit C
            if (globalT > arrivalC.at(0)):
                #Transmit C
                globalT = globalT + SCD.DIFS + backoffA + SCD.frame + SCD.SIFS + SCD.ACK
                transmissionC+= 1

        elif(arrivalC.at(0) > arrivalA.at(0)): # if C
            #Transmit C
            globalT = arrivalC.at(0)
            globalT = globalT + SCD.DIFS + backoffA + SCD.frame + SCD.SIFS + SCD.ACK 
            transmissionC+= 1


            #if global timer (after transmitting C) is past A's arrival time, transmit A
            if (globalT > arrivalA.at(0)):
                #Transmit A
                globalT = globalT + SCD.DIFS + backoffA + SCD.frame + SCD.SIFS + SCD.ACK
                transmissionA+= 1
'''
def SingleCollisionDCF(parameters, FrameRate):
    
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
                channel.idle_count = parameters.FrameSize + parameters.SIFS + parameters.ACK
                if A.state == State.transmit:
                    A.state = State.idle
                if C.state == State.transmit:
                    C.state = State.idle
            continue
    
        if A.state == State.readyTransmit:
            if A.backoff is None:
                A.calcBackoff()
            A.state = State.waitTransmit
    
        if C.state == State.readyTransmit:
            if C.backoff is None:
                C.calcBackoff()
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
                        #transmit
                        A.state = State.transmit
        if C.state == State.waitTransmit:
            if channel.is_idle:
                C.difs_duration -= 1
            else:
                C.difs_duration = 4
            if C.difs_duration <= 0:
                C.backoff -= 1
                if C.backoff <= 0:
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

