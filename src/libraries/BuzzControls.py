import streams
import pwm

#create a serial port stream with default parameters

# the pin where the buzzer is attached to
buzzerpin = D19.PWM
a4 = 440
c5 = 550
e5 = 660
a5 = 880


sequences = {
            1 : [a4,c5,e5,a5,a5,e5,c5,a4],
            2 : [a4,e5,a4,c5,a4],
            3 : [a4,c5,e5,a5,a5,e5,c5,a4,e5,c5,e5,c5,a4,c5]
            }
            
pinMode(buzzerpin,OUTPUT) #set buzzerpin to output mode


note = 0 

def reset():
    """Stops the buzzer from playing"""
    
    pwm.write(buzzerpin,0,0)
    note = 0

def sing(melody,alarm):
    """Reproduces the chosen song while an alarm is set"""
    
    song = sequences[melody]
    while alarm.is_set():
        frequency = song[note]
        period=1000000//frequency #we are using MICROS so every sec is 1000000 of micros. // is the int division, pwm.write period doesn't accept floats
        #set the period of the buzzer and the duty to 50% of the period
        pwm.write(buzzerpin,period,period//2,MICROS)
        note = (note+1)%len(song)
        sleep(500)
    reset()
        
        
