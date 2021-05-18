class MemorizedAlarm:
    def __init__(self,hour,minute,color = "blue",song = 3):
        self.hour = hour
        self.minute = minute
        if color not in ["red", "blue", "green", "yellow", "white", "magenta",  "cyan"]:
            print("Color not Found, fallback to blue") 
            self.color = "blue"
        else:
            self.color=color
        if song in range(0,3):
            self.song = song
        else:
            print("song not found, fallback to 3")
            self.song=3
        self.isDelayed = False
        
    def setSong(self,song):
        self.song = song
        
    def setColor(self,color):
        self.color = color
        
