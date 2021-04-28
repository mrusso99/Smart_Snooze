import streams
from LedControls import Leds
from BuzzerControls import BuzzControls

streams.serial()


while True:
    Leds.color_selector("red")
    sleep(500)
    Leds.color_selector("magenta")
    sleep(500)
    Leds.color_selector("blue")
    sleep(500)
    Leds.color_selector("cyan")
    sleep(500)
    Leds.color_selector("green")
    sleep(500)
    Leds.color_selector("yellow")
    sleep(500)
    Leds.color_selector("white")
    sleep(500)