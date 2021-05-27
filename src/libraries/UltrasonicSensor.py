

class UltrasonicSensor:
    
    @c_native("HCRS04_readDistanceRaw", ["UltrasonicSensor.c"], [])
    def _getDistanceRaw(trig, echo):
        pass
    
    def getDistanceRaw(self):
        return UltrasonicSensor._getDistanceRaw(self.trigger, self.echo)
    
    def getDistanceCM(self):
        return self.getDistanceRaw() / 58
    
    def getDistanceINCH(self):
        return self.getDistanceRaw() / 148
    
    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        
        pinMode(self.trigger, OUTPUT)
        pinMode(self.echo, INPUT)
        
