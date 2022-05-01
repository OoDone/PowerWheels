import pygame
import bluetooth
from Logger import Logger
import sys
from time import sleep

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

stickDeadband = 2

logger = Logger("clientLog")

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
def enableRobot():
    logger.info("Controller: Sending Enable Request!")
def toggleAutonMode():
    logger.info("Controler: Autonomous Mode Toggled!")
def disableAutonMode():
    logger.info("Controler: Disabled Autonomous Mode!")
    
def stopRobot():
    sock.send("s") #FIXME
    
def squareDown():
    sock.send("ho")#FIXME
    
def squareUp():
    sock.send("ho")#FIXME
 
#enableRobot()

def loop():
    sleep(0.02) #sleep 20 ms
    try:
        speed = float(round(j.get_axis(1) * -100))
        direction = float(round(j.get_axis(3) * 100)) #axis 0
        if direction < stickDeadband and direction > -stickDeadband:
            direction = 0.0
        if speed > -101 and direction > -101:
            logger.info("PRE: M:" + str(speed) + ":D:" + str(direction))
            #FIXME SEND DATA
    except:
        logger.warn("EXCEPTION: LOOP FUNCTION INFO: sysinfo: " + str(sys.exc_info()[0]) + " speed: " + str(speed) + " direction: " + str(direction))
    
    
while True:
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
              
  
               
    except KeyboardInterrupt:
        stopRobot()
        print("EXITING NOW")
        j.quit()
        x.toString()