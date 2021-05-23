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


def watchForAlarms(alarmsList, alarm, lock_on_RTC):
    """To be called in a thread, it checks if the current time corresponds to a time in which the alarm should be set on and sets it on"""
    
    while True:
        lock_on_RTC.acquire()
        print("Lock acquired on library")
        currentTime = ds.get_time()
        lock_on_RTC.release()
        print("lock released")
        for memorizedAlarm in alarmsList:
            if currentTime[0] == memorizedAlarm.hour and currentTime[1] == memorizedAlarm.minute:
                if not alarm.is_set():
                    alarm.set()
                    #Add the threads to set the LED and the Buzzer properly based on the chosen alarmTime and to check if the user wants a snooze.
                    #thread(hcsr04.checkDelays,memorizedAlarm,alarmsList,alarm)
                    thread(Leds.setAlarmColor,memorizedAlarm.color,alarm)
                    print("thread1")
                    thread(BuzzControls.sing,memorizedAlarm.song,alarm)
                    #Removes the delayedAlarm when the alarm clears.
                    thread(checkDelays,memorizedAlarm,alarmsList,alarm)
                    print("thread3")
                    if memorizedAlarm.isDelayed:
                        while alarm.is_set():
                            sleep(1000)
                        alarmsList.remove(memorizedAlarm)
                    sleep(60000)
        sleep(1000)
        

def checkDelays(memorizedAlarm,alarmsList,alarm):
        #TODO: Check how to get the information about the checkDelay
        print("entro nel checkdelay")
        while alarm.is_set():
            if delayDetected(10):
                
                newAlarm = MemorizedAlarm.MemorizedAlarm(memorizedAlarm.hour,memorizedAlarm.minute + 1, memorizedAlarm.color, memorizedAlarm.song)
                newAlarm.isDelayed = True
                alarm.clear()
                alarmsList.append(newAlarm)
                print(newAlarm.hour, newAlarm.minute)




def delayDetected(distanceCM):
    if prox.getDistanceCM() < distanceCM:
        return True

        
