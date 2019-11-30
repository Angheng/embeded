import time

class PID:

    def __init__( self, kP=1, kI=0, kD=0 ):
        self.kP = kP
        self.kI = kI
        self.kD = kD

    def initialize(self):
        self.current = time.time()
        self.prev = self.current

        self.prevErr = 0

        self.cP = 0
        self.cI = 0
        self.cD = 0

    def update(self, err, sleep=0.2):
        time.sleep(sleep)

        self.current = time.time()
        deltaTime = self.current - self.prev

        deltaErr = err - self.prevErr

        self.cP = err

        self.cI += err * deltaTime
        self.cD = ( deltaErr / deltaTime ) if deltaTime > 0 else 0

        self.prev = self.current
        self.prevErr = err
        
        return sum([
            self.kP * self.cP,
            self.kI * self.cI,
            self.kD * self.cD
            ])
