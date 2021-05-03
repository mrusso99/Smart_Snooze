import maxim.ds1307 import ds1307
import streams
streams.serial()
from src.libraries.LedControls import Leds
from src.libraries.BuzzerControls import BuzzControls
import threading

ds=ds1307.DS1307(I2C0)
ds.start()

button = D5
pinMode(button,INPUT_PULLDOWN)


alarm = threading.Event()
thread(Leds.loop,alarm)
thread(BuzzControls.sing,2,alarm)


def printOnLCD():
    "LCD todo, function that prints everything we need on the LCD"
    while True
        print("%02d:%02d:%02d - %02d/%02d/%d - %d"%ds.get_time())
        sleep(1000)

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
