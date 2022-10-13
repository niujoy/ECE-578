import numpy as np
import math
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
        arrivalA_P.append(np.random.poisson(lam=1))  #TODO: random poisson inputs not doing what we want (may have inputs wrong / knowledge of what is outputted)
        print(arrivalA_P)
        arrivalA_sec = [(-1/L * math.log(1 - x)) for x in arrivalA_P] #TODO: math domain error
        arrivalA_S = [(math.ceil(y / 10e-6)) for y in arrivalA_sec] #TODO: math domain error

    # TODO: sum arrivalA_S with its previous values

    return arrivalA_S
    
def arrivalTimeC(totalSlots, L): # pass in lambda

    arrivalC_P = []  #poisson
    arrivalC_sec = [] #seconds
    arrivalC_S = [] #slots

    while (np.sum(arrivalC_S) < totalSlots): 
        arrivalC_P.append(np.random.poisson(1, 1)) #TODO
        arrivalC_sec = [(-1/L * math.log(1 - x)) for x in arrivalC_P] #TODO
        arrivalC_S = [(math.ceil(y / 10e-6)) for y in arrivalC_sec] #TODO

    # TODO: sum arrivalA_S with its previous values

    return [arrivalC_S]



def main():
    '''
    main is set up so far for SingleCollision DCF 
    we can put in a separate function later if we want, wasn't sure which separation approach was best
    '''
    slotdur = 10e-6
    totalSlots = 10 / slotdur 
    frame = 1000 * 8 / 10e-6  #number of slots of frame 1000 bytes
    globalT = 0 # Global timer (in slots)
    transmissionA = 0 # Count for number of transmissions
    transmissionC = 0 # Count for number of transmissions

    arrivalA = arrivalTimeA(totalSlots, 100) # totalSlots, lambda
    arrivalC = arrivalTimeC(totalSlots, 100) # totalSlots, lambda

    while (globalT < totalSlots):

        # hard coded process for first index
        # TODO: loop correctly
        if(arrivalA.at(0) > arrivalC.at(0)):
            # Transmit A
            
            transmissionA+=1

            #if global timer (after transmitting A) is past C's arrival time, transmit C
            if (globalT > arrivalC.at(0)):
                #Transmit C
                transmissionC+= 1

        elif(arrivalC.at(0) > arrivalA.at(0)):

            transmissionC+= 1

            #if global timer (after transmitting C) is past C's arrival time, transmit A
            if (globalT > arrivalA.at(0)):
                #Transmit A
                transmissionA+= 1

       
        



if __name__ == "__main__":
    main()