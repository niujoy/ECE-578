import math

def calcFairnessIndex(NumASuccesses,NumCSuccesses,MaxSlots,parameters):
    A = (NumASuccesses*parameters.FrameSize)/MaxSlots
    C = (NumCSuccesses*parameters.FrameSize)/MaxSlots
    return A/C
            
def calcThroughputBits(successes, FrameSizeByte, time, scale):
    return 8*(successes * FrameSizeByte/time)/scale