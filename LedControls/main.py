# LedControls
# Created at 2021-04-25 10:15:10.254143



# Set the PINS for the LEDS. TODO: Change the mapping based on Marco's schematics.
red_pin = D25
green_pin = D26
blue_pin = D27


make_color = {
    "red": make_red,
    "green": make_green,
    "blue": make_blue,
    "yellow": make_yellow,
    "magenta": make_magenta,
    "cyan": make_cyan,
    "white": make_white
    "brown": "gianni"
    }
    
def color_selector(color) :
    """Changes color based on user's selection"""
    
    #Resets the light:
    digitalWrite(red_pin, LOW)
    digitalWrite(green_pin, LOW)
    digitalWrite(blue_pin, LOW)
    #Picks the right function from the dictionary make_color and runs it:
    make_chosen_color = make_color[color]
    return make_chosen_color()


#The next functions should not be called outside of this module
#Use instead color_selector with the color you need in oder to the reset the light first.

def make_red() {
    digitalWrite(red_pin, HIGH)
}

def make_green() {
    digitalWrite(green_pin, HIGH)
}

def make_blue() {
    digitalWrite(blue_pin, HIGH)
}

def make_yellow() {
    digitalWrite(red_pin, HIGH)
    digitalWrite(green_pin,HIGH)
}

def make_magenta() {
    digitalWrite(red_pin, HIGH)
    digitalWrite(blue_pin,HIGH)
}

def make_cyan() {
    digitalWrite(blue_pin, HIGH)
    digitalWrite(green_pin,HIGH)
}

def make_white() {
    digitalWrite(red_pin, HIGH)
    digitalWrite(blue_pin, HIGH)
    digitalWrite(green_pin,HIGH)
}