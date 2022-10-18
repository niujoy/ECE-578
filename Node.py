import math
import numpy as np
from queue import Queue
from enum import Enum

# calculate idle: FrameSize + SIFS + ACK + RTS + CTS + (2x SIFS)
class Channel:
    def __init__(self, parameters):
        self.is_idle = True
        self.idle_count = parameters.FrameSize + parameters.SIFS + parameters.ACK + 2 + 2 + 1 + 1 

# state definitions
class State(Enum):
    idle = 0
    readyTransmit = 1 # ready to transmit
    waitTransmit = 2  # waiting to transmit
    transmit = 3      # currently transmitting
    RTS = 4           # sending RTS
    NAV = 5           # waiting for NAV
    
# node definition
class Node:

    def __init__(self, parameters, FrameRate, seed=None):
        # will produce the same random set instead of random sets every time like np.random.rand(4)
        np.random.seed(seed) 
        
        # parameter dependent
        self.ack = parameters.ACK
        self.backoff = None
        self.difs_duration = parameters.DIFS
        self.cw_min= parameters.CW_min
        self.cw_max = parameters.CW_max
        self.cw = self.cw_min
        self.sifs_duration = parameters.SIFS
        self.FrameDistribution = self.calcDistribution(FrameRate,parameters.MaxTime)

        self.FrameIndex = 0
        self.state = State.idle
        self.queue = Queue(maxsize=len(self.FrameDistribution))
        self.transmit_count = 0
        self.valid = True
        self.RTS_end = 0
        self.NAV = 0
        self.CTS_count = 0


    def checkState(self, slot, otherNode):
        if slot == self.FrameDistribution[self.FrameIndex]:
            self.queue.put(slot)
            if self.FrameIndex < len(self.FrameDistribution) - 1:
                self.FrameIndex += 1 
        if self.state == State.transmit:
            return
        elif not self.queue.empty() and not (self.state == State.waitTransmit or self.state == State.RTS) and not otherNode.transmit_count >1:
            self.state = State.readyTransmit


    def calcBackoff(self):
        self.backoff = np.random.randint(0, (min(self.cw, self.cw_max))-1)
        
        
    def calcDistribution(self, lam, t, t_slot=10e-6):
        u = np.random.uniform(size=(lam*t))
        x = [-(1/lam) * math.log(1-i) for i in u]
        x = [math.ceil(i/t_slot) for i in x]
        x = list(np.cumsum(x))
        return x
    
    def calcTransmit(self, parameters):
        return parameters.FrameSize + parameters.SIFS + parameters.ACK

    def calcNAV(self, parameters):
        return 2 + parameters.SIFS + 2 + parameters.SIFS + self.calcTransmit(parameters)
    
    def collision(self):
        self.state = State.idle
        self.cw = self.cw * 2
        self.backoff = None
        self.valid = True
        self.difs_duration = 4
    
    def reset(self):
        self.state = State.idle
        self.cw = self.cw_min
        self.backoff = None
        self.valid = True
        self.difs_duration = 4