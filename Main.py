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

from BluetoothServer import BluetoothServer

#from Constants import Constants
logger = Logger("/home/pi/Desktop/logs/robotLog")
blServer = BluetoothServer(logger)
driveControl = DriveControl(logger)
constants = Constants()
buzzer = Buzzer(logger)
auton = AutonMain(logger)
autonMode = 1
autonEnabled = False
enabled = False
disconnected = False
client_socket = None
logger.info("Robot | Code: Main.py Init")
#time.sleep(1)
def enableRobot():
    buzzer.customBuzz(0.05,0.05, 3) #3 long enable robot
    global enabled
    enabled = True
    logger.info("Robot | Enabled Robot.")
    if constants.isTestingMode == True:
        logger.info("Robot | Robot in Test Mode!")
    if constants.isTestingMode == False and blServer.getStatus() == True:
        client_socket.send("enable")

def disableRobot():
    global enabled
    enabled = False
    driveControl.stopRobot()
    logger.info("Robot | Disabled Robot.")
    
while(1):
    if blServer.getStatus():
        if client_socket is None:
            client_socket = blServer.getClientSocket()
            client_socket.send("ready")
            #auton.setSocket(client_socket)
    if constants.isTestingMode == True:
        if enabled == False:
            enableRobot()
        x=bytes(input(), 'utf-8')
    else:
        x=blServer.return_data()
    if x == None:
        if constants.isTestingMode == False:
            logger.info("Bluetooth: disconnected!")
            buzzer.buzz(0.1, 2)
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
    elif x==bytes('xd','UTF-8'):
        driveControl.steerServoPerc(100)
        logger.info("Test steer 100%")
    else:
        client_socket.send("<<<  wrong data  >>>")
        client_socket.send("please enter the defined data to continue.....")
