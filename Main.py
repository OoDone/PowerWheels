import bluetooth
import RPi.GPIO as GPIO
from time import sleep
import time
import os 
from sensor import ultrasonicRead
from Logger import Logger
import pigpio
import BluetoothServer
#from Constants import Constants
autonMode = 1
motorNeutralSpeed = 1500
motorMinSpeed = 1000
motorMaxSpeed = 2000
enabled = False
autonEnabled = False
disconnected = False
ultrasonicSensorEnabled = False
servoPin = 18
ESC = 4
servoNeutralPosition = 1700 #1488 for 556-2420 & 1700 for 1500-1900
directionTicksPer = 2 #(Ticks of rotation)/100 #100 is for input value
os.system ("sudo pigpiod")
time.sleep(1)
logger = Logger("robotLog")

GPIO.setmode(GPIO.BCM)
bd_addr = "DC:A6:32:6B:38:BD"  #"B8:27:EB:D6:57:CE" 
#B8:27:EB:6B:AB:4B
uuid = "42b58f76-b26d-11ea-b733-cb205305bc99"
port = 1

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0)

    
def enableRobot():
    #enabledAlert(0.5, 3) #3 long enable robot
    enabled = True
    logger.info("Robot: Robot Enabled")
    client_socket.send("Robot: Enabled Robot")
    

    
    
logger.info("\n")
logger.info("Robot Program Started...")
logger.info("\n")


while(1):
    x=BluetoothServer.return_data()
    if x == None:
        logger.info("Bluetooth: disconnected!")
        pi.set_servo_pulsewidth(ESC, 0)
        disconnected = True
        client_socket, address = server_socket.accept()
        if disconnected == True:
            logger.info("Bluetooth: Reconnected!")

    elif bytes(':','UTF-8') in x:
        #MAIN DRIVE CODE.
        speed = x.decode('UTF-8').split(':')[2].replace("'",'')
        direction = x.decode('UTF-8').split(':')[4].replace("'",'')
        if enabled == True:
            try:
                speed = float(speed)
                direction = float(direction)
            except:
                speed = 0.0
                direction = 0.0
                logger.warn("Exception: speed or direction not a number")
            if speed > 0:#0
                pi.set_servo_pulsewidth(ESC, speed*5+motorNeutralSpeed)
            elif speed < 0: #0
                pi.set_servo_pulsewidth(ESC, motorNeutralSpeed + speed * 5)
            else:
                pi.set_servo_pulsewidth(ESC, 0)
            if direction < 0:
                directionPosition = -direction * directionTicksPer + servoNeutralPosition #* 9.36 + 1489 # TEMP  
            else:
                directionPosition = servoNeutralPosition - direction * directionTicksPer   # 1489 - direction * directionTicksPer #* 9.36        #1489 mid servo position
            pi.set_servo_pulsewidth(servoPin, directionPosition)
                #Set servo To directionPosition
                
    elif x==bytes('s', 'UTF-8'):
        logger.info("Stopping robot...")
        pi.set_servo_pulsewidth(ESC, 0)
        enabled = False
        x='z'

    elif x==bytes('en', 'UTF-8'):
        logger.info("Robot Enabled")
        enabled = True
        enableRobot()
        x='z'

    elif x==bytes('e', 'UTF-8'):
        GPIO.cleanup()
        break
    elif x==bytes('ho','UTF-8'):
        if buzzer == False:
            #GPIO.output(buzzerPin,GPIO.HIGH)
            buzzer = True
        elif buzzer == True:
            #GPIO.output(buzzerPin,GPIO.LOW)
            buzzer = False
    elif x==bytes('au','UTF-8'):
        #Auton Mode
        #MainAuton.enableAuton(True, 1)
        #autonEnabled = MainAuton.getAutonEnabled()
    else:
        client_socket.send("<<<  wrong data  >>>")
        client_socket.send("please enter the defined data to continue.....")
