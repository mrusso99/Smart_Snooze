class hcsr04:
    
    @c_native("HCRS04_readDistanceRaw", ["hcsr04.c"], [])
    def _getDistanceRaw(trig, echo):
        pass
    
    def getDistanceRaw(self):
        return hcsr04._getDistanceRaw(self.trigger, self.echo)
    
    def getDistanceCM(self):
        return self.getDistanceRaw() / 58
    
    def getDistanceINCH(self):
        return self.getDistanceRaw() / 148
    
    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        
        pinMode(self.trigger, OUTPUT)
        pinMode(self.echo, INPUT)

    def checkDelays(memorizedAlarm,alarmsList,alarm):
        #TODO: Check how to get the information about the checkDelay
        while alarm.is_set():
            if delayDetected:
                alarm.clear()
                newAlarm = MemorizedAlarm(memorizedAlarm.hour,memorizedAlarm.minute + 5, memorizedAlarm.color, memorizedAlarm.song)
                newAlarm.isDelayed = True
                alarmsList.append(newAlarm)
        