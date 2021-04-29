# LedControls
# Created at 2021-04-25 10:15:10.254143



# Set the PINS for the LEDS. TODO: Change the mapping based on Marco's schematics.
red_pin = D23
green_pin = D22
blue_pin = D21

pinMode(red_pin,OUTPUT)
pinMode(green_pin,OUTPUT)
pinMode(blue_pin,OUTPUT)

#The next functions should not be called outside of this module
#Use instead color_selector with the color you need in oder to the reset the light first.

def make_red() :
    digitalWrite(red_pin, HIGH)

def make_green() :
    digitalWrite(green_pin, HIGH)


def make_blue() :
    digitalWrite(blue_pin, HIGH)


def make_yellow() :
    digitalWrite(red_pin, HIGH)
    digitalWrite(green_pin,HIGH)

def make_magenta() :
    digitalWrite(red_pin, HIGH)
    digitalWrite(blue_pin,HIGH)


def make_cyan() :
    digitalWrite(blue_pin, HIGH)
    digitalWrite(green_pin,HIGH)


def make_white() :
    digitalWrite(red_pin, HIGH)
    digitalWrite(blue_pin, HIGH)
    digitalWrite(green_pin,HIGH)

make_color = {
    "red": make_red,
    "green": make_green,
    "blue": make_blue,
    "yellow": make_yellow,
    "magenta": make_magenta,
    "cyan": make_cyan,
    "white": make_white
    }
    
def color_selector(color) :
    """Changes color based on user's selection"""
    
    #Resets the light:
    digitalWrite(red_pin, LOW)
    digitalWrite(green_pin, LOW)
    digitalWrite(blue_pin, LOW)
    #Picks the right function from the dictionary make_color and runs it:
    make_chosen_color = make_color[color]
    make_chosen_color()
    
    
def loop():
    """Call it in a thread to test threads with the LED"""
    
    while True:
        color_selector("red")
        sleep(500)
        color_selector("green")
        sleep(500)       
        color_selector("blue")
        sleep(500)        
        color_selector("yellow")
        sleep(500)
        color_selector("magenta")
        sleep(500)
        color_selector("cyan")
        sleep(500)       
        color_selector("white")
        sleep(500)        



