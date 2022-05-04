import pygame
import bluetooth
from Logger import Logger
import sys
from time import sleep
from timer import Timer

#0 = X
#1 = CIRCLE
#2 = TRIANGLE
#3 = SQUARE
#4 = L1
#5 = R1
#6 = L2
#7 = R2
#8 = SHARE
#9 = OPTIONS
#10 = PS4 BUTTON
#11 = LEFT ANALOG PRESS 
#12 = RIGHT ANALOG PRESS



bluetoothAddress = "DC:A6:32:6B:38:BD" #Mine "DC:A6:32:6B:38:BD"      #School other"B8:27:EB:D6:57:CE"  
#School server: B8:27:EB:6B:AB:4B
stickDeadband = 3
logger = Logger("/home/pi/Desktop/logs/clientLog")
joy = False
speed = False
direction = False
connected = False
ready = False
start = False

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
    global joy
    global ready
    ready = False
    connected = False
    joy = False
    timer = Timer()
    timer.start()
    while not connected:
        if timer.hasElapsed(3):
            timer.reset()
            try:
                if not connected:
                    pygame.init()
                    j = pygame.joystick.Joystick(0)
                    j.init()
                    joy = True
            except:
                pygame.quit()
                joy = False
                logger.warning("No Joystick Detected")
            try:
                if not connected and joy:
                    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                    sock.connect((bluetoothAddress, 1))
                    sock.setblocking(False)
                    joy = False
                    connected = True
                    timer.stop()
                    logger.info("Client: Connected To Robot!")
            except:
                logger.warning("Bluetooth: Cannot find Bluetooth Server")
        else:
            return

def enableRobot():
    if connected:
        if ready:
            sock.send("en")
            logger.info("Client: Sending Enable Request!")
        else:
            logger.info("Client: Robot Still Starting.")
    else:
        logger.info("Client: Not Connected To Robot")

def disableRobot():
    if connected:
        sock.send("di")
        logger.info("Client: Sending Disable Request!")
    else:
        logger.info("Client: Not Connected To Robot")
def toggleAutonMode():
    if connected:
        sock.send("au")
        logger.info("Client: Autonomous Mode Toggled!")
    else:
        logger.info("Client: Not Connected To Robot")
def disableAutonMode():
    logger.info("Client: DOES NOTHING: Disabled Autonomous Mode!")
    
def stopRobot():
    if connected:
        sock.send("s")
    else:
        logger.info("Client: Not Connected To Robot")

def squareDown():
    if connected:
        sock.send("xd")
    else:
        logger.info("Client: Not Connected To Robot")

def squareUp():
    if connected:
        sock.send("ho")
    else:
        logger.info("Client: Not Connected To Robot")

#enableRobot()

def loop():
    loopTimer = Timer()
    loopTimer.start() 
    if loopTimer.hasElapsed(0.02):
    #sleep(0.02) #sleep 20 ms
        loopTimer.reset()
        global speed
        global direction
        try:
            speed = float(round(j.get_axis(1) * -100))
            direction = float(round(j.get_axis(3) * 100)) #axis 0
            if direction < stickDeadband and direction > -stickDeadband:
                direction = 0.0
            if speed >= -100 and direction >= -100:
                #logger.info("PRE: M:" + str(speed) + ":D:" + str(direction))
                sock.send(":M:" + str(speed) + ":D:" + str(direction))
        except:
            logger.warn("EXCEPTION: LOOP FUNCTION INFO: sysinfo: " + str(sys.exc_info()[0]) + " speed: " + str(speed) + " direction: " + str(direction))
    else:
        logger.info("Else")
        
x = None
circle = None
square = None
triangle = None  
while connected:
    try: 
        sock.getpeername()
        connected = True
    except:
        connected = False
        init()
    try:
        loop()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if j.get_button(0) and not x: #X
                    disableRobot()
                    x = True
                if j.get_button(1) and not circle: #circle
                     enableRobot()
                     circle = True
                if j.get_button(2) and not triangle: #Triangle
                    toggleAutonMode()
                    triangle = True
                if j.get_button(3) and not square: #Square
                    disableAutonMode()
                    square = True
            elif event.type == pygame.JOYBUTTONUP:
                if x and not j.get_button(0): #X
                    x = False
                elif circle and not j.get_button(1): #circle
                    circle = False
                elif triangle and not j.get_button(2): #triangle
                    triangle = False
                elif square and not j.get_button(3): #square
                    square = False
                
        x=return_data()
        if x is not None:
            if bytes(':','UTF-8') in x:
                xd = x.decode('UTF-8').split(":")[1]
                print("Collision warning " + xd + " cm")
            elif bytes('enable','UTF-8') in x:
                xd = x.decode('UTF-8')
                logger.info("Robot | Enabled Robot.")
            elif bytes('disable','UTF-8') in x:
                xd = x.decode('UTF-8')
                logger.info("Robot | Disabled Robot.")
            elif bytes('ready','UTF-8') in x:
                xd = x.decode('UTF-8')
                ready = True
                logger.info("Robot | Robot Started.")
            else:
                try:
                    data = return_data().replace("b'", "").replace("'","")
                    logger.info("Robot | " + data)
                except:
                    logger.warn("Cannot use .replace Line 103")
              
  
               
    except KeyboardInterrupt:
        disableRobot()
        print("EXITING NOW")
        j.quit()
        x.toString()

while True:
    if not start:
        init() 
        start = True
        
