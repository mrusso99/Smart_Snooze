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
import internet
from zdm import zdm


internet.internet.connect()

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
    "changeDistancePostponement": changeDistancePostponement,
    "changeMinsPostponement": changeMinsPostponement
}

tags = ["temperatura","alarm"]



device = zdm.Device(jobs_dict = dict, condition_tags=tags)


    # just start it
device.connect()

disp = lcd.lcd(i2cport = I2C1)


button = D5
pinMode(button,INPUT_PULLDOWN)

alarmList = [MemorizedAlarm.MemorizedAlarm(8,31,"magenta",3),MemorizedAlarm.MemorizedAlarm(8,30,"blue",2),MemorizedAlarm.MemorizedAlarm(19,55,"blue",2),]

alarm = threading.Event()

def setAlarmOff():
    """clears the alarm,resets every component involved in it"""
    if alarm.is_set():
        print("comincio ad annullare l'allarme..")
        alarm.clear()
        Leds.reset()
        BuzzControls.reset()
        print("allarme annullato")
        
        
#Whenever the button is pressed, clear the alarm:
onPinRise(button,setAlarmOff)
thread(RTC.watchForAlarms,alarmList,alarm)
# loop forever


time = RTC.ds.get_time()
oldHour = time[0]
oldMinute = time[1]
disp.clear()
disp.message("%02d:%02d"%time)
temperatura = DigitalTemperature.read()
disp.message("%d Celsius"%temperatura,line=2)


while True:
    time = RTC.ds.get_time()
    if oldHour != time[0] or oldMinute != time[1]:
        disp.clear()
        disp.message("%02d:%02d"%time)
        temperatura = DigitalTemperature.read()
        disp.message("%d Celsius"%temperatura,line=2)
        payload={"temperatura":temperatura}
        device.publish(payload, "temperatura")
    oldHour = time[0]
    oldMinute = time[1]
    sleep(1000)


