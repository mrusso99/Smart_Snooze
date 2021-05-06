import streams
streams.serial()
from src.libraries import RTC
from src.libraries import Leds
from src.libraries import BuzzControls
from src.libraries import DigitalTemperature
from src.libraries import hcsr04
import threading

button = D5
pinMode(button,INPUT_PULLDOWN)

class MemorizedAlarm:
    def __init__(self,hour,minute,color,song):
        self.hour = hour
        self.minute = minute
        self.color = color
        self.song = song
        self.isDelayed = False
        
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

sens = hcsr04.hcsr04(D23, D22)

while False:
    cm = sens.getDistanceCM()
    
    print("Distance: %.2f" % cm)
    
    sleep(1000)
    
while True:
    print("%02d:%02d:%02d - %02d/%02d/%d - %d"%RTC.ds.get_time())
    DigitalTemperature.read()
    sleep(1000)
