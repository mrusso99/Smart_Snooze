import streams


trigger=D27
echo=D26

pinMode(trigger, OUTPUT)
pinMode(echo, INPUT)
s=streams.serial()



def read_distance() :
    while True: 
    	digitalWrite(trigger,HIGH) 
    	sleep(10,MICROS)
    	digitalWrite(trigger,LOW)
    	counter = 0
    	while digitalRead(echo) == LOW:
        	sleep(10,MICROS)
        	counter += 1
        	if counter >= 2500:
            		return -1
    
    	counter=0
    	while digitalRead(echo) == HIGH:
        	sleep(10,MICROS)
        	counter += 1
        	if counter >= 3800:
            		break
        
    return(counter/5.8)
    
