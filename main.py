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


internet.internet.connect()

agent = zdm.Device()
    # just start it
agent.connect()




#TODO: retrieve memorizedAlarms from MQTT server
alarmList = [MemorizedAlarm.MemorizedAlarm(3,16,"magenta",3),MemorizedAlarm.MemorizedAlarm(10,39,"blue",2)]

def insertAlarm(hour,minute,color = "white",song = 3):
    newAlarm = MemorizedAlarm.MemorizedAlarm(hour,minute,color,song)
    alarmList.append(newAlarm)

def deleteAlarm(hour,minute):
    for alarm in alarmList:
        if (alarm.hour == hour and alarm.minute == minute):
            alarmList.remove(alarm)

dict = {
    "readTemp" : DigitalTemperature.read,
    "readTime" : RTC.ds.get_time,
    "insertAlarm" : insertAlarm,
    "deleteAlarm" : deleteAlarm
}

tags = ["temperatura"]

device = zdm.Device() # just start it 
device.connect() 
while True: # use the agent to publish values to the ZDM
# Just open the device page from VSCode and check that data is incoming
    v = random(0,100)
    device.publish({"value":v}, "test")
    print("Published",v) 
    sleep(5000) # The agent automatically handles connections and reconnections 

disp = lcd.lcd(i2cport = I2C1)


button = D5
pinMode(button,INPUT_PULLDOWN)


<<<<<<< Updated upstream




        
#TODO: retrieve memorizedAlarms from MQTT server
alarmList = [MemorizedAlarm.MemorizedAlarm(3,16,"magenta",3),MemorizedAlarm.MemorizedAlarm(10,37,"blue",2)]
=======
>>>>>>> Stashed changes

alarm = threading.Event()

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

sens = hcsr04.hcsr04(D23, D22)

while False:
    cm = sens.getDistanceCM()
    
    print("Distance: %.2f" % cm)
    
    sleep(1000)

while True:
    disp.clear()
    disp.message("%02d:%02d:%02d"%RTC.ds.get_time())
    temp=DigitalTemperature.read()
    disp.message("%d Celsius"%DigitalTemperature.read(),line = 2)
    agent.publish({"temperatura":temp}, "temperatura")
    sleep(5000)


