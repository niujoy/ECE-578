
class SingleDomain:
    def __init__(self, DIFS, SIFS, backoff1, backoff2, ACK, frame):
        self.DIFS = 4
        self.SIFS = 1
        self.backoff1 = 0
        self.backoff2 = 0
        self.ACK = 2
        self.frame = 1000 * 8 # 1000 bytes


        # outputs: throughput, rate

'''
Single Collision Domain:
A ----> B
C ----> D

Send DIFS to sense other channels
Count backoff 
assume Channel A has lowest backoff --> transmit (C channel pauses count)
Send data, SIFS, ACK on A

IF backoffs the same
    reset and double CW

'''

def SingleCollisionDCF( L ):
    Acount = 0
    Ccount = 0
