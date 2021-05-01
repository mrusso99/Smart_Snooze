from src.libraries.LedControls import Leds
from src.libraries.BuzzerControls import BuzzControls
import threading

button = D5
pinMode(button,INPUT_PULLDOWN)


alarm = threading.Event()
thread(Leds.loop,alarm)
thread(BuzzControls.sing,2,alarm)


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
#while True:
    #sleep(5000)
