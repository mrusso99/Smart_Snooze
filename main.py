from src.libraries.LedControls import Leds
from src.libraries.BuzzerControls import BuzzControls
import threading


alarm = threading.Event()
thread(Leds.loop,alarm)
thread(BuzzControls.sing,2,alarm)

# loop forever
while True:
    alarm.set()
    print("setting...")
    sleep(10000)
    alarm.clear()
    BuzzControls.reset()
    Leds.reset()
    print("clearing...")
    sleep(10000)

    

