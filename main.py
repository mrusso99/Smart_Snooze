import streams
streams.serial()
from src.libraries.LedControls import Leds
from src.libraries.BuzzerControls import BuzzControls
import threading

button = D5
pinMode(button,INPUT_PULLDOWN)

#every alarm must follow this syntax: ((hours,minutes),color,song)
alarmList = [((13,01),"magenta",2),((17,18),"blue",3)   ]

alarm = threading.Event()

def setAlarmOff():
    """clears the alarm,resets every component involved in it"""
    
    if alarm.is_set:
        alarm.clear()
        Leds.reset()
        BuzzControls.reset()
        
        
#Whenever the button is pressed, clear the alarm:
onPinRise(button,setAlarmOff)

# loop forever
alarm.set()
thread(Leds.setAlarmColor,"magenta",alarm)
thread(BuzzControls.sing,3,alarm)
#while True:
    #sleep(5000)
