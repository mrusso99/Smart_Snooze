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


lock_on_RTC= threading.Lock()
lock_on_temp= threading.Lock()

alarmList = [MemorizedAlarm.MemorizedAlarm(17,20,"magenta",3),MemorizedAlarm.MemorizedAlarm(10,39,"blue",2)]
alarm = threading.Event()





distanceCM=50
minsPostponement=5

def on_timestamp(device, timestamp):
    print("RCV time:",timestamp) 
    iso_date=timestamp["rfc3339"]
    year=iso_date[0:4]
    month=iso_date[5:7]
    day=iso_date[8:10]
    hour=iso_date[11:13]
    minute=iso_date[14:16]
    second=iso_date[17:19]
    RTC.ds.set_time(int(hour),int(minute),int(second),int(day),int(month),int(year),1)


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
        """return{"res":"New alarm inserted"}"""
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
    
def changeDistancePostponement(device, arg):
    if "distance" in arg:
        if arg["distance"] > 100 and arg["distance"]< 10:
            return{"err": "Distance not allowed, pick a value between 10 and 100"}
            print("Distance not allowed, pick value between 10 and 100")
        else:
            distanceCM=arg["distance"]
            return{"res":"Distance changed, new value:" + distanceCM}
    else:

        print("Wrong payload format")
        
def changeMinsPostponement(device, arg):
    if "minutes" in arg:
        if arg["minutes"] > 30 and arg["minutes"]<= 0:
            return{"err": "Error, pick a value under 30 minutes and greater than 0"}
            print("Error, pick a value under 30 minutes and greater than 0")
        else:
            minsPostponement=arg["minutes"]
            return{"res":"Value changed, new value:" + minsPostponement}
    else:
        return{"err":"Wrong payload format"}
        print("Wrong payload format")
    
dict = {
    "readTemp" : DigitalTemperature.read,
    "readTime" : RTC.ds.get_time,
    "insertAlarm" : insertAlarm,
    "deleteAlarm" : deleteAlarm,
    "setTime": setTime,
    "changeDistancePostponement": changeDistancePostponement,
    "changeMinsPostponement": changeMinsPostponement
}

tags = ["temperatura","alarm"]




internet.internet.connect()

device = zdm.Device(jobs_dict = dict,condition_tags = tags, on_timestamp=on_timestamp)
    # just start it
device.connect()

def sendTempToZDM(device,tags):
    while True:    
        lock_on_temp.acquire()
        temp=DigitalTemperature.read()
        lock_on_temp.release()
        payload={"temperatura":temp}
        device.publish(payload, tags[0])
        sleep(5000)

thread(sendTempToZDM,device,tags)

disp = lcd.lcd(i2cport = I2C1)


button = D5
pinMode(button,INPUT_PULLDOWN)

        


def setAlarmOff():
    """clears the alarm,resets every component involved in it"""

    if alarm.is_set():
        alarm.clear()
        Leds.reset()
        BuzzControls.reset()
        
device.request_timestamp()
#Whenever the button is pressed, clear the alarm:
onPinRise(button,setAlarmOff)
thread(RTC.watchForAlarms,alarmList,alarm,lock_on_RTC)





while True:
    disp.clear()
    lock_on_RTC.acquire()
    print("Lock acquired in main")
    disp.message("%02d:%02d:%02d"%RTC.ds.get_time())
    lock_on_RTC.release()
    print("Lock released")
    lock_on_temp.acquire()
    disp.message("%d Celsius"%DigitalTemperature.read(),line = 2)
    lock_on_temp.release()
    sleep(1000)


