import streams
from src.libraries import SnoozeManager
from src.libraries import DigitalTemperature
from src.libraries import lcd
from src.libraries import LedControls
from src.libraries import BuzzerControls
import threading
from src.libraries import MemorizedAlarm
import internet
from zdm import zdm

streams.serial()

minsAndDistance=[1,50]


internet.internet.connect()


def on_timestamp(device, timestamp):
    print("RCV time:",timestamp) 
    iso_date=timestamp["rfc3339"]
    year=iso_date[0:4]
    month=iso_date[5:7]
    day=iso_date[8:10]
    hour=int(iso_date[11:13])+2
    minute=iso_date[14:16]
    second=iso_date[17:19]
    SnoozeManager.ds.set_time(hour,int(minute),int(second),int(day),int(month),int(year),1)

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
        print("New alarm inserted,", arg)
        device.publish({"hour":newAlarm.hour,"minute":newAlarm.minute,"color":newAlarm.color,"song":newAlarm.song},"alarm")
        return{"res":"New alarm inserted"}
    else:
        print("Wrong payload,", arg)
        return {"err":"Wrong payload format"}
        
        
def deleteAlarm(device,arg):
    if "hour" in arg and "minute" in arg:
        hour=arg["hour"]
        minute=arg["minute"]
        trovato=False
        for alarm in alarmList:
            if alarm.hour==hour and alarm.minute==minute:
                trovato=True 
                alarmList.remove(alarm)
                print("Alarm deleted,", arg)
                payload = {"hour":alarm.hour,"minute":alarm.minute,"color":alarm.color,"song":alarm.song}
                device.publish(payload,"deletedAlarm")
        if not trovato:
            print("Error 404: Alarm not found")
            return{"err":"Error 404: Alarm not found"}
        else:
            return{"res":"Alarm deleted"}
    else:
        print("Wrong payload,", arg)
        return{"err":"Wrong payload format"}
        
def editAlarm(device,arg):
    if "hour" in arg and "minute" in arg:
        hour=arg["hour"]
        minute=arg["minute"]
        trovato=False
        for alarm in alarmList:
            if alarm.hour==hour and alarm.minute==minute:
                trovato=True
                payload = {"hour":alarm.hour,"minute":alarm.minute,"color":alarm.color,"song":alarm.song}
                device.publish(payload,"deletedAlarm")
                if "color" in arg:
                    alarm.setColor(arg["color"])
                if "song" in arg:
                    alarm.setSong(arg["song"])
                payload = {"hour":alarm.hour,"minute":alarm.minute,"color":alarm.color,"song":alarm.song}
                device.publish(payload,"alarm")
        if not trovato:
            print("Error 404: Alarm not found")
            return{"err":"Error 404: Alarm not found"}
        else:
            return{"res":"Alarm deleted"}
    else:
        print("Wrong payload,", arg)
        return{"err":"Wrong payload format"}

def changeDistancePostponement(device, arg):
    if "distance" in arg:
        if arg["distance"] > 100 or arg["distance"]< 10:
            return{"err": "Distance not allowed, pick a value between 10 and 100"}
            print("Distance not allowed, pick value between 10 and 100")
        else:
            minsAndDistance[1]=arg["distance"]
            return{"res":"Distance changed, new value"}
    else:
        return{"err":"Wrong payload format"}
        print("Wrong payload format")
        
def changeMinsPostponement(device, arg):
    if "minutes" in arg:
        if arg["minutes"] > 30 or arg["minutes"]<= 0:
            return{"err": "Error, pick a value under 30 minutes and greater than 0"}
            print("Error, pick a value under 30 minutes and greater than 0")
        else:
            minsAndDistance[0]=arg["minutes"]
            return{"res":"Value changed, new value"}
    else:
        return{"err":"Wrong payload format"}
        print("Wrong payload format")
    
dict = {
    "insertAlarm" : insertAlarm,
    "deleteAlarm" : deleteAlarm,
    "editAlarm": editAlarm,
    "changeDistancePostponement": changeDistancePostponement,
    "changeMinsPostponement": changeMinsPostponement
}

tags = ["temperatura","alarm"]



device = zdm.Device(jobs_dict = dict, condition_tags=tags, on_timestamp=on_timestamp)

    # just start it
device.connect()

device.request_timestamp()

disp = lcd.lcd(i2cport = I2C1)


button = D5
pinMode(button,INPUT_PULLDOWN)

alarmList = [MemorizedAlarm.MemorizedAlarm(8,31,"magenta",3),MemorizedAlarm.MemorizedAlarm(8,30,"blue",2),MemorizedAlarm.MemorizedAlarm(19,55,"blue",2),]

alarm = threading.Event()

def setAlarmOff():
    """clears the alarm,resets every component involved in it"""
    if alarm.is_set():
        alarm.clear()
        LedControls.reset()
        BuzzerControls.reset()
        
        
#Whenever the button is pressed, clear the alarm:
onPinRise(button,setAlarmOff)
thread(SnoozeManager.watchForAlarms,alarmList,alarm,minsAndDistance)
# loop forever


time = SnoozeManager.ds.get_time()
oldHour = time[0]
oldMinute = time[1]
disp.clear()
disp.message("%02d:%02d"%time)
temperatura = DigitalTemperature.read()
disp.message("%d Celsius"%temperatura,line=2)


while True:
    time = SnoozeManager.ds.get_time()
    if oldHour != time[0] or oldMinute != time[1]:
        disp.clear()
        disp.message("%02d:%02d"%time)
        temperatura = DigitalTemperature.read()
        disp.message("%d Celsius"%temperatura,line=2)
        if not alarm.is_set():
            payload={"temperatura":temperatura}
            device.publish(payload, "temperatura")
    oldHour = time[0]
    oldMinute = time[1]
    sleep(1000)