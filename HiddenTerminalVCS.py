class MultipleDomain:
    def __init__(self, DIFS, SIFS, backoff1, backoff2, ACK, RTS, CTS, frame):
        self.DIFS = 4
        self.SIFS = 1
        self.backoff1 = 0
        self.backoff2 = 0
        self.ACK = 2
        self.RTS = 2
        self.CTS = 2
        self.frame = 1000 * 8 # 1000 bytes
        
        # outputs: throughput, rate

