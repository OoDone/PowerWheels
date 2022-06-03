#!/usr/bin/python

import time
from drive.DriveControl import DriveControl
from Logger import Logger
from Variables import Constants
from other.Buzzer import Buzzer
from autonomous.AutonMain import AutonMain
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO
try:
    from BluetoothServer import BluetoothServer
except:
    print("Cannot Import BluetoothServer")

#from Constants import Constants
try:
    logger = Logger("/home/pi/Desktop/logs/robotLog")
except:
    logger = Logger("robotLog")
driveControl = DriveControl(logger)
constants = Constants()
if not constants.isTestingMode:
    blServer = BluetoothServer(logger)
buzzer = Buzzer(logger)
auton = AutonMain(logger)
autonMode = 1
autonEnabled = False
enabled = False
disconnected = False
client_socket = None
logger.info("Robot | Code: Main.py Init")
GPIO.setmode(GPIO.BCM)         #Set GPIO pin numbering
GPIO.setup(constants.RobotConstants().killSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def enableRobot():
    global enabled
    if not enabled:
        buzzer.customBuzz(0.05,0.05, 3) #3 long enable robot
        enabled = True
        logger.info("Robot | Enabled Robot.")
        if constants.isTestingMode == True:
            logger.info("Robot | Robot in Test Mode!")
        if constants.isTestingMode == False and blServer.getStatus() == True:
            client_socket.send("enable")
    else:
        logger.info("Robot | Robot Already Enabled.")

def disableRobot():
    global enabled
    if enabled:
        enabled = False
        driveControl.stopRobot()
        auton.enableAuton(False)
        GPIO.cleanup() #FIXME might not work
        logger.info("Robot | Disabled Robot.")
        try:
            if constants.isTestingMode == False and blServer.getStatus() == True:
                client_socket.send("disable")
        except:
            logger.warning("Robot | Couldnt Inform Client Of New Status: Disabled")
    else:
        logger.info("Robot | Robot Already Disabled")
   
while(1):
    try:
        if auton.isEnabled():
            auton.loop()
    except:
        y=1
    #try:
    #GPIO.setmode(GPIO.BCM)         #Set GPIO pin numbering
    #GPIO.setup(constants.RobotConstants().killSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    input_state = GPIO.input(constants.RobotConstants().killSwitchPin) #Read and store value of input to a variable
    logger.info("Input_State: " + str(input_state))
    if input_state and not constants.isTestingMode: #True is not on(Robot disabled)
        #global enabled
        if enabled:
            disableRobot() #Disable robot every time its enabled while the kill switch is active(In off position)
    if constants.isTestingMode == True:
        if enabled == False:
            enableRobot()
        x=bytes(input(), 'utf-8')
    else:
        x=blServer.return_data()
        if blServer.getStatus():
            if client_socket is None:
                client_socket = blServer.getClientSocket()
                client_socket.send("ready")
                logger.info("READY")
    if x == None:
        if constants.isTestingMode == False:
            logger.info("Bluetooth: disconnected!")
            buzzer.buzz(0.1, 2)
            auton.enableAuton(False)
            driveControl.stopRobot()
            disconnected = True
            blServer.setStatus(False)
            client_socket, address = blServer.reconnect()
            if disconnected == True:
                client_socket.send("ready")
                blServer.setStatus(True)
                buzzer.buzz(0.3, 1)
                logger.info("Bluetooth: Reconnected!")
    elif bytes(':','UTF-8') in x:
        if enabled == True and not auton.isEnabled():
            driveControl.driveRobot(x)
    elif x==bytes('s', 'UTF-8'):
        driveControl.stopRobot()
        logger.info("Stopping robot...")
        x='z'
    elif x==bytes('en', 'UTF-8'):
        logger.info("Enabling Robot...")
        enableRobot()
        x='z'
    elif x==bytes('di', 'UTF-8'):
        logger.info("Disabling Robot...")
        disableRobot()
        x='z'
    elif x==bytes('e', 'UTF-8'):
        GPIO.cleanup()
        break
    elif x==bytes('ho','UTF-8'):
        if buzzer == False:
            buzzer = True
        elif buzzer == True:
            buzzer = False
    elif x==bytes('au','UTF-8'):
        logger.info("Auton")
        auton.setAutonMode(0)
        auton.enableAuton(True)
    elif x==bytes('ad','UTF-8'):
        auton.enableAuton(False)
    else:
        client_socket.send("<<<  wrong data  >>>")
        client_socket.send("please enter the defined data to continue.....")
    #except:
        #logger.info("Robot | Error in Main Loop, Shutting down program(Change to continue and not crash?).")
        #disableRobot()
        #crash.toString()
