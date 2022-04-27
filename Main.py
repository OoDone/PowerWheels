import time
from drive.DriveControl import DriveControl
from Logger import Logger
from Constants import Constants
from other.Buzzer import Buzzer
from autonomous.AutonMain import AutonMain
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO

from BluetoothServer import BluetoothServer

#from Constants import Constants
logger = Logger("robotLog")
blServer = BluetoothServer(logger)
driveControl = DriveControl(logger)
constants = Constants()
buzzer = Buzzer(logger)
auton = AutonMain(logger)
autonMode = 1
autonEnabled = False
enabled = False
disconnected = False
logger.info("Robot | Code: Main.py Init")
time.sleep(1)
def enableRobot():
    buzzer.buzz(0.5, 3) #3 long enable robot
    global enabled
    enabled = True
    logger.info("Robot | Enabled Robot.")
    if constants.isTestingMode == True:
        logger.info("Robot | Robot in Test Mode!")
    #if constants.isTestingMode == False and blServer.getStatus() == True:
        #client_socket.send("Robot: Enabled Robot")

def disableRobot():
    global enabled
    enabled = False
    driveControl.stopRobot()
    logger.info("Robot | Disabled Robot.")
    GPIO.cleanup()
    
while(1):
    if constants.isTestingMode == True:
        if enabled == False:
            enableRobot()
        x=bytes(input(), 'utf-8')
    else:
        x=blServer.return_data()
    if x == None:
        logger.info("Bluetooth: disconnected!")
        driveControl.stopRobot()
        disconnected = True
        if constants.isTestingMode == False:
            client_socket = blServer.getServerSocket()
        if disconnected == True:
            logger.info("Bluetooth: Reconnected!")
    elif bytes(':','UTF-8') in x:
        if enabled == True:
            driveControl.driveRobot(x)
    elif x==bytes('s', 'UTF-8'):
        logger.info("Stopping robot...")
        disableRobot()
        x='z'
    elif x==bytes('en', 'UTF-8'):
        logger.info("Enabling Robot...")
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
        logger.info("Auton")
        auton.setAutonMode(0)
        auton.enableAuton(True)
        #MainAuton.enableAuton(True, 1)
        #autonEnabled = MainAuton.getAutonEnabled()
    else:
        client_socket.send("<<<  wrong data  >>>")
        client_socket.send("please enter the defined data to continue.....")
