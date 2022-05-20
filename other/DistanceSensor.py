from asyncio.log import logger
import time
import RPi.GPIO as GPIO
from time import sleep




class DistanceSensor:
    trigPin = 16
    echoPin = 12
    MAX_DISTANCE = 10000
    timeOut=MAX_DISTANCE*60
    def __init__(self, Logger):
        global logger
        logger = Logger
        logger.info("Robot | Code: DistanceSensor.py Init")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigPin, GPIO.OUT) # set trigPin to output mode
        GPIO.setup(self.echoPin, GPIO.IN)

    """ This module detects objects using the ultrasonic and sends feedback to the main(radar) module"""
    def pulseIn(self, pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
        t0 = time.time()
        while(GPIO.input(pin) != level):
            if((time.time() - t0) > timeOut*0.000001):
                return 0
        t0 = time.time()
        while(GPIO.input(pin) == level):
            if((time.time() - t0) > timeOut*0.000001):
                return 0
        pulseTime = (time.time() - t0)*1000000
        return pulseTime

    def getSonar(self): #get the measurement results of ultrasonic module,with unit: cm
        GPIO.output(self.trigPin,GPIO.HIGH) #make trigPin send 10us high level
        sleep(0.00001) #10us
        GPIO.output(self.trigPin,GPIO.LOW)
        pingTime = self.pulseIn(self.echoPin,GPIO.HIGH,self.timeOut) #read plus time of echoPin
        distance = pingTime * 340.0 / 2.0 / 10000.0 # the sound speed is 340m/s, andcalculate distance (cm)
        return distance
    
    def ultrasonicRead(self):
        #print(self.getSonar())
        return self.getSonar()