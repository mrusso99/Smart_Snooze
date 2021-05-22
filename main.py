import streams
streams.serial()
from src.libraries import RTC
from src.libraries import Leds
from src.libraries import BuzzControls
from src.libraries import DigitalTemperature
from src.libraries import hcsr04
from src.libraries import lcd
import threading
from src.libraries import MemorizedAlarm
from zdm import zdm
import internet
from zdm import zdm
import datetime
import re

alarmList = [MemorizedAlarm.MemorizedAlarm(3,16,"magenta",3),MemorizedAlarm.MemorizedAlarm(10,39,"blue",2)]
alarm = threading.Event()



def on_timestamp(device, timestamp):
    print("RCV time:",timestamp) 
    
    return timest


def insertAlarm(device, arg):
    color="blue"
    song=3 
    if "hour" in arg and "minute" in arg:
        if "song" in arg:
            song=arg["song"]
        if "color" in arg:
            color=arg["color"]
        newAlarm = MemorizedAlarm.MemorizedAlarm(arg["hour"],arg["minute"],color,song)
        alarmList.append(newAlarm)
        return{"res":"New alarm inserted"}
        print("New alarm inserted,", arg)
    else:
        return {"err":"Wrong payload format"}
        print("Wrong payload,", arg)
        
def deleteAlarm(device,arg):
    if "hour" in arg and "minute" in arg:
        hour=arg["hour"]
        minute=arg["minute"]
        trovato=False
        for alarm in alarmList:
            if alarm.hour==hour and alarm.minute==minute:
                alarmList.remove(alarm)
                print("Alarm deleted,", arg)
                trovato=True 
        if not trovato:
            print("Error 404: Alarm not found")
            return{"err":"Error 404: Alarm not found"}
        else:
            return{"res":"Alarm deleted"}
    else:
        print("Wrong payload,", arg)
        return{"err":"Wrong payload format"}
        
def setTime(device, arg):
    
    if "hour" in arg and "minutes" in arg and "seconds" and "day" in arg and "month" in arg and "year" in arg and "day_of_week" in arg:
        print("formato corretto")
        RTC.ds.set_time(arg["hours"],arg["minutes"],arg["seconds"],arg["day"],arg["month"],arg["year"],arg["day_of_week"])
    
        
dict = {
    "readTemp" : DigitalTemperature.read,
    "readTime" : RTC.ds.get_time,
    "insertAlarm" : insertAlarm,
    "deleteAlarm" : deleteAlarm,
    "setTime": setTime
}
tags = ["temperatura"]

internet.internet.connect()

device = zdm.Device(jobs_dict = dict,condition_tags = tags, on_timestamp=on_timestamp)
    # just start it
device.connect()

#TODO: retrieve memorizedAlarms from MQTT server





disp = lcd.lcd(i2cport = I2C1)


button = D5
pinMode(button,INPUT_PULLDOWN)




        
#TODO: retrieve memorizedAlarms from MQTT server

def setAlarmOff():
    """clears the alarm,resets every component involved in it"""
    
    if alarm.is_set():
        alarm.clear()
        Leds.reset()
        BuzzControls.reset()
        
        
#Whenever the button is pressed, clear the alarm:
onPinRise(button,setAlarmOff)
thread(RTC.watchForAlarms,alarmList,alarm)
# loop forever



utc_timestamp=device.request_timestamp()






while True:
    disp.clear()
    disp.message("%02d:%02d:%02d"%RTC.ds.get_time())
    temp=DigitalTemperature.read()
    disp.message("%d Celsius"%DigitalTemperature.read(),line = 2)
    payload={"temperatura":temp}
    device.publish(payload, tags[0])
    sleep(5000)


