import threading
from maxim.ds1307 import ds1307
from src.libraries import Leds
from src.libraries import BuzzControls
from src.libraries import hcsr04
from src.libraries import MemorizedAlarm
import streams

ds=ds1307.DS1307(I2C0)
ds.start()
prox=hcsr04.hcsr04(23,22)
def watchForAlarms(alarmsList, alarm,minsAndDistance):
    """To be called in a thread, it checks if the current time corresponds to a time in which the alarm should be set on and sets it on"""
    
    while True:
        currentTime = ds.get_time()
        for memorizedAlarm in alarmsList:
            if currentTime[0] == memorizedAlarm.hour and currentTime[1] == memorizedAlarm.minute:
                if not alarm.is_set() and not memorizedAlarm.alreadyRang:
                    print("setto l'allarme")
                    alarm.set()
                    #Removes the delayedAlarm from AlarmList in order to not memorize it
                    if memorizedAlarm.isDelayed:
                        alarmsList.remove(memorizedAlarm)
                    thread(checkDelays,memorizedAlarm,alarmsList,alarm,minsAndDistance[1])
                    memorizedAlarm.alreadyRang = True
                    print("allarme settato")
                    Leds.color_selector(memorizedAlarm.color)
                    print("ho settato i led")
                    BuzzControls.sing(memorizedAlarm.song,alarm)
                    Leds.reset()
                    print("Sono alla fine!!!!")
            if currentTime[0] == (memorizedAlarm.hour + minsAndDistance[0])%24:
                    memorizedAlarm.alreadyRang = False
        sleep(1000)
        

def checkDelays(memorizedAlarm,alarmsList,alarm,distanceCM):
        """"Checks if the user delays the alarm and sets the new alarm"""
        delayAmount = 1
        while alarm.is_set():
            if delayDetected(distanceCM):
                newMinute = (memorizedAlarm.minute + delayAmount)%60
                newHour = memorizedAlarm.hour
                if (memorizedAlarm.minute > newMinute):
                    newHour = (memorizedAlarm.hour + 1)%24
                newAlarm = MemorizedAlarm.MemorizedAlarm(newHour,newMinute, memorizedAlarm.color, memorizedAlarm.song)
                newAlarm.isDelayed = True
                alarm.clear()
                alarmsList.append(newAlarm)
                print(newAlarm.hour, newAlarm.minute)

def delayDetected(distanceCM):
    if prox.getDistanceCM() < distanceCM:
        return True
        