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
import fs
from zdm import zdm

internet.internet.connect()

agent = zdm.Device()
    # just start it
agent.connect()




disp = lcd.lcd(i2cport = I2C1)


button = D5
pinMode(button,INPUT_PULLDOWN)




    # read an existing file in read mode
    f = fs.open("/zerynth/snoozes.txt", "r")
    # read it all and print it
    print(f.read()) 
    # close the file
    f.close()

    # create a new file and read it back
    f = fs.open("/zerynth/test02.txt","w")
    f.write("first row: test 01\n")
    f.write("second row: test 02\n")
    f.close()

    f = fs.open("/zerynth/test02.txt", "r")
    print(f.read())
    f.close()

    sleep(5000)


        
#TODO: retrieve memorizedAlarms from MQTT server
alarmList = [MemorizedAlarm.MemorizedAlarm(3,16,"magenta",3),MemorizedAlarm.MemorizedAlarm(10,37,"blue",2)]

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


