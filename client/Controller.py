import pygame
import bluetooth
from Logger import Logger
import sys
from time import sleep
import asyncio
from timer import Timer

#0 = SQUARE
#1 = X
#2 = CIRCLE
#3 = TRIANGLE
#4 = L1
#5 = R1
#6 = L2
#7 = R2
#8 = SHARE
#9 = OPTIONS
#10 = LEFT ANALOG PRESS
#11 = RIGHT ANALOG PRESS
#12 = PS4 ON BUTTON
#13 = TOUCHPAD PRESS



bluetoothAddress = "DC:A6:32:6B:38:BD"  #"B8:27:EB:D6:57:CE"  
#B8:27:EB:6B:AB:4B
stickDeadband = 2
logger = Logger("clientLog")
blue = False
speed = False
direction = False
connected = False


def return_data():
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            #print(data)
            return data
    except OSError:
        pass



def init():
    global sock
    global j
    global connected
    connected = False
    timer = Timer()
    timer.start()
    pygame.init()
    while not connected:
        if timer.hasElapsed(5):
            timer.reset()
            try:
                if not connected:
                    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                    sock.connect((bluetoothAddress, 1))
                    sock.setblocking(False)
                    blue = True
            except:
                logger.warning("Bluetooth: Cannot find Bluetooth Server")
            try:
                if not connected:
                    j = pygame.joystick.Joystick(0)
                    j.init()
                    if blue:
                        blue = False
                        connected = True
            except:
                logger.warning("No Joystick Detected")


def enableRobot():
    sock.send("en")
    logger.info("Controller: Sending Enable Request!")
def toggleAutonMode():
    sock.send("au")
    logger.info("Controller: Autonomous Mode Toggled!")
def disableAutonMode():
    logger.info("Controller: Disabled Autonomous Mode!")
    
def stopRobot():
    sock.send("s")
    
def squareDown():
    sock.send("ho")
    
def squareUp():
    sock.send("ho")
 
#enableRobot()

def loop():
    sleep(0.02) #sleep 20 ms
    global speed
    global direction
    try:
        speed = float(round(j.get_axis(1) * -100))
        direction = float(round(j.get_axis(3) * 100)) #axis 0
        if direction < stickDeadband and direction > -stickDeadband:
            direction = 0.0
        if speed > -101 and direction > -101:
            #logger.info("PRE: M:" + str(speed) + ":D:" + str(direction))
            sock.send(":M:" + str(speed) + ":D:" + str(direction))
    except:
        logger.warn("EXCEPTION: LOOP FUNCTION INFO: sysinfo: " + str(sys.exc_info()[0]) + " speed: " + str(speed) + " direction: " + str(direction))

init()   
while connected:
    try: 
        sock.getpeername()
        connected = True
    except:
        connected = False
    try:
        loop()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if j.get_button(0): #IDK
                    squareDown()
                if j.get_button(1): #circle
                     enableRobot()
                if j.get_button(2): #Triangle wtf
                    toggleAutonMode()
                if j.get_button(3): #Square
                    disableAutonMode()
            elif event.type == pygame.JOYBUTTONUP:
                if j.get_button(0): #square
                    squareUp()
                
        x=return_data()
        if x is not None:
            if bytes(':','UTF-8') in x:
                xd = x.decode('UTF-8').split(":")[1]
                print("Collision warning " + xd + " cm")
            else:
                try:
                    data = return_data().replace("b'", "").replace("'","")
                    logger.info(data)
                except:
                    logger.warn("Cannot use .replace Line 103")
              
  
               
    except KeyboardInterrupt:
        stopRobot()
        print("EXITING NOW")
        j.quit()
        x.toString()
        
