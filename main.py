import streams
streams.serial()
from src.libraries import RTC
from src.libraries import Leds
from src.libraries import BuzzControls
from src.libraries import DigitalTemperature
import threading

button = D5
pinMode(button,INPUT_PULLDOWN)


#every alarm must follow this syntax: ((hours,minutes),color,song)
class MemorizedAlarm:
    def __init__(self,hour,minute,color,song):
        self.hour = hour
        self.minute = minute
        self.color = color
        self.song = song
        
    def setSong(self,song):
        self.song = song
        
    def setColor(self,color):
        self.color = color
        
#TODO: retrieve memorizedAlarms from MQTT server
alarmList = [MemorizedAlarm(16,37,"magenta",3),MemorizedAlarm(10,43,"blue",2)]

alarm = threading.Event()

def setAlarmOff():
    """clears the alarm,resets every component involved in it"""
    
    if alarm.is_set:
        alarm.clear()
        Leds.reset()
        BuzzControls.reset()
        
        
#Whenever the button is pressed, clear the alarm:
onPinRise(button,setAlarmOff)
thread(RTC.watchForAlarms,alarmList,alarm)
# loop forever

while True:
    print("%02d:%02d:%02d - %02d/%02d/%d - %d"%RTC.ds.get_time())
    DigitalTemperature.read()
    sleep(1000)
