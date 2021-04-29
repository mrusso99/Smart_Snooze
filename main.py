from src.libraries.LedControls import Leds
from src.libraries.BuzzerControls import BuzzControls
import threading

ledThread = threading.Thread(target=Leds.loop)
buzzThread = threading.Thread(target=BuzzControls.sing,args=3)

ledThread.start()
buzzThread.start()
# loop forever
while True:
    # print something
    print("Hello Zerynth!")
    # sleep 1 second
    sleep(1000)

