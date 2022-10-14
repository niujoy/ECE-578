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

       
        



if __name__ == "__main__":
    main()