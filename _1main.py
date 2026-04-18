from machine import PWM,Pin
import time, utime

#Pin Layout
left = PWM(Pin(3))
right = PWM(Pin(1))
triggerL = Pin(14,Pin.OUT)  
echoL = Pin(15,Pin.IN)
triggerR = Pin(16,Pin.OUT)  
echoR = Pin(17,Pin.IN)

#Speeds for servo (Ramkrishna)
SpeedStop = 1500000    
Speedfastfor = 2000000
Speedslowfor = 1600000
SpeedMediumfor = 1750000
Speedfastback = 1000000
Speedslowback = 1400000
Speedmedback = 1250000

#Frequency for servo (Ramkrishna)
frequency = 50
left.freq(frequency)
right.freq(frequency)

#Directions 
def stop():
    left.duty_ns(SpeedStop)
    right.duty_ns(SpeedStop)
    
def forward():
    left.duty_ns(Speedslowfor)
    right.duty_ns(Speedmedback)

def right_turn():
    left.duty_ns(SpeedStop)     
    right.duty_ns(Speedmedback)

def back():
    left.duty_ns(Speedmedback)  
    right.duty_ns(SpeedMediumfor)
    
def left_turn():
    left.duty_ns(SpeedMediumfor)     
    right.duty_ns(SpeedStop)

#Ultrasonic Function (Dieme)
def distanceSensor(trigger, echo):
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()

    while echo.value() == 0: 
        off = utime.ticks_us()
    while echo.value() == 1: 
        on = utime.ticks_us()
    timepassed = on - off 
    distance = (timepassed * 0.0343) / 2 
    return distance

#Main Loop (Ramkrishna)
while True:
    #Setting up US Sensor
    Ldistance = distanceSensor(triggerL, echoL)
    Rdistance = distanceSensor(triggerR, echoR)
    print("Left:", Ldistance, "cm")
    print("Right:", Rdistance, "cm")
    
    if Ldistance > 10:
        #Condition for Right turn if left edge detected
        stop()
        utime.sleep_ms(300)
        
        back()  
        utime.sleep_ms(200)  
        
        right_turn()  
        utime.sleep_ms(200)            
        
        stop()
        utime.sleep_ms(300)
    elif Rdistance > 10:
        #Condition for Left turn if right edge detected
        stop()
        utime.sleep_ms(300)
        
        back()  
        utime.sleep_ms(200)  
        
        left_turn()  
        utime.sleep_ms(200)            
       
        stop()
        utime.sleep_ms(300)   
    else:
        #Condition if no edge detected
        forward()

    utime.sleep_ms(1)

