import threading
from maxim.ds1307 import ds1307
from src.libraries import Leds
from src.libraries import BuzzControls

ds=ds1307.DS1307(I2C0)
ds.start()

def watchForAlarms(alarmsList, alarm):
    """To be called in a thread, it checks if the current time corresponds to a time in which the alarm should be set on and sets it on"""
    
    while True:
        currentTime = ds.get_time()
        for memorizedAlarm in alarmsList:
            if currentTime[0] == memorizedAlarm.hour and currentTime[1] == memorizedAlarm.minute:
                if not alarm.is_set():
                    alarm.set()
                    #TODO: Add here the threads to set the LED and the Buzzer properly based on the chosen alarmTime
                    thread(Leds.setAlarmColor,memorizedAlarm.color,alarm)
                    thread(BuzzControls.sing,memorizedAlarm.song,alarm)
                    sleep(60000)
        sleep(1000)
        

def printOnLCD():
    "TODO: LCD function that prints everything we need on the LCD"
    
    while True:
        print("%02d:%02d:%02d - %02d/%02d/%d - %d"%ds.get_time())
        sleep(1000)