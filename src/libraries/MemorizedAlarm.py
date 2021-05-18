class MemorizedAlarm:
    def __init__(self,hour,minute,color = "blue",song = 3):
        self.hour = hour
        self.minute = minute
        self.color = color
        self.song = song
        self.isDelayed = False
        
    def setSong(self,song):
        self.song = song
        
    def setColor(self,color):
        self.color = color
        
