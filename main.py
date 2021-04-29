from src.libraries.LedControls import Leds
from src.libraries.BuzzerControls import BuzzControls
import threading

thread(Leds.loop)
thread(BuzzControls.sing,2)

# loop forever
while True:
    #print something
    print("Hello Zerynth!")
    # sleep 1 second
    sleep(1000)

