import numpy as np
import math



class SingleDomain:
    def __init__(self, DIFS, SIFS, backoff1, backoff2, ACK, frame):
        self.DIFS = 4
        self.SIFS = 1
        self.ACK = 2
        self.frame = 1000 * 8 / 10e-6  #number of slots of frame 1000 bytes
        # outputs: throughput, rate

def arrivalTimeA(totalSlots, L): # pass in lambda
    '''
    set values drawn from poission distribution (Ua, Uc)
    Translate Ua,Uc to exponential values (Xa, Xc)
        Xa = -(1/lambda) * ln(1-Ua)
    Translate Xa,Xc (which are in seconds) to slots
        **Round up to the nearest slot
        Divide each value by slot duration (10us)
    '''
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


'''
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
        