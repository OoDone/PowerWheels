import pygame
from Logger import Logger
import sys
from time import sleep

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

#10 = LEFT ANALOG PRESS
#11 = RIGHT ANALOG PRESS
#12 = PS4 ON BUTTON
#13 = TOUCHPAD PRESS

stickDeadband = 2

logger = Logger("clientLog")

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
    
#enableRobot()

def loop():
    sleep(0.2) #sleep 20 ms
    #try:
        #speed = float(round(j.get_axis(1) * -100))
        #direction = float(round(j.get_axis(3) * 100)) #axis 0
        #if direction < stickDeadband and direction > -stickDeadband:
           # direction = 0.0
        #if speed > -101 and direction > -101:
            #logger.info("Data: M:" + str(speed) + ":D:" + str(direction))
            #FIXME SEND DATA
    #except:
        #logger.warn("EXCEPTION: LOOP FUNCTION INFO: sysinfo: " + str(sys.exc_info()[0]) + " speed: " + str(speed) + " direction: " + str(direction))
    
x = None
circle = None
square = None
triangle = None
butt4 = None
butt5 = None
butt6 = None
while True:
    try:
        #loop()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if j.get_button(0) and not x: #X
                    logger.info("X Button DOWN")
                    x = True
                if j.get_button(1) and not circle: #circle
                     logger.info("Circle Button DOWN")
                     circle = True
                if j.get_button(2) and not triangle: #Triangle wtf
                    logger.info("Triangle Button DOWN")
                    triangle = True
                if j.get_button(3) and not square: #Square
                    logger.info("Square Button DOWN")
                    square = True
                if j.get_button(11) and not butt4: #4
                    logger.info("butt11 Button DOWN")
                    butt4 = True
                if j.get_button(12) and not butt5: #R1
                    logger.info("butt12 Button DOWN")
                    butt5 = True
                if j.get_button(13) and not butt6: #6
                    logger.info("butt13 Button DOWN")
                    butt6 = True
            elif event.type == pygame.JOYBUTTONUP:
                if x and not j.get_button(0): #X
                    logger.info("X Button UP")
                    x = False
                elif circle and not j.get_button(1): #circle
                    logger.info("Circle Button UP")
                    circle = False
                elif triangle and not j.get_button(2): #triangle
                    logger.info("Triangle Button UP")
                    triangle = False
                elif square and not j.get_button(3): #square
                    logger.info("Square Button UP")
                    square = False
                elif butt4 and not j.get_button(11): #4
                    logger.info("butt11 Button UP")
                    butt4 = False
                elif butt5 and not j.get_button(12): #R1
                    logger.info("butt12 Button UP")
                    butt5 = False
                elif butt6 and not j.get_button(13): #6
                    logger.info("butt13 Button UP")
                    butt6 = False
  
               
    except KeyboardInterrupt:
        print("EXITING NOW")
        j.quit()
        x.toString()