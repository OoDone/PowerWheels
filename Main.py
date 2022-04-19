import bluetooth
import RPi.GPIO as GPIO
from time import sleep
import time
from sensor import ultrasonicRead
from Logger import Logger
import BluetoothServer
from drive import DriveControl
#from Constants import Constants
driveControl = DriveControl()
autonMode = 1
enabled = False
autonEnabled = False
disconnected = False
ultrasonicSensorEnabled = False
servoPin = 18
servoNeutralPosition = 1700 #1488 for 556-2420 & 1700 for 1500-1900
directionTicksPer = 2 #(Ticks of rotation)/100 #100 is for input value
time.sleep(1)
logger = Logger("robotLog")

def enableRobot():
    #enabledAlert(0.5, 3) #3 long enable robot
    enabled = True
    logger.info("Robot: Robot Enabled")
    client_socket.send("Robot: Enabled Robot")
    
while(1):
    x=BluetoothServer.return_data()
    if x == None:
        logger.info("Bluetooth: disconnected!")
        driveControl.stopRobot()
        disconnected = True
        client_socket, address = server_socket.accept()
        if disconnected == True:
            logger.info("Bluetooth: Reconnected!")
    elif bytes(':','UTF-8') in x:
        if enabled == True:
            driveControl.driveRobot(x)
    elif x==bytes('s', 'UTF-8'):
        logger.info("Stopping robot...")
        driveControl.stopRobot()
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
