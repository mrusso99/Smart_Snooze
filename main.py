import BuzzControls
from LedControls import *
import streams

streams.serial()


while True:
    print("in da loop")
    #digitalWrite(D23,HIGH)
    #sleep(4000)
    #Leds.color_selector("red")
    sleep(500)
    #Leds.color_selector("magenta")
    sleep(500)
    Leds.color_selector("blue")
    sleep(500)
    Leds.color_selector("cyan")
    sleep(500)
    Leds.color_selector("green")
    sleep(500)
    #Leds.color_selector("yellow")
    sleep(500)
    Leds.color_selector("white")
    sleep(1000)