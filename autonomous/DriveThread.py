#!/usr/bin/python

import os
import threading



start = False
stop = False
driveRobot = False
driveDirection = False #False is forwards
class AutonDrive:
    def __init__(self, Logger):
        global logger
        logger = Logger
        logger.info("Robot | Code: DriveAuton Class Init")
    
    def stopRobot():
        global stop
        stop = True
        logger.info("DriveThread: Stopping robot..")

    def driveRobot(isReverse):
        #if isReverse is true, drive backwards, else drive forwards
        global driveRobot
        global driveDirection
        driveRobot = True
        driveDirection = isReverse
        logger.info("DriveThread: Driving Robot...")
        #MAKE FUNCTIONS IN THE DRIVETHREAD CLASS TO CALL INSTEAD OF SETTTING GLOBAL VARIABLES


class DriveThread(threading.Thread):
    def __init__(self, Logger, threadID, Start):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "Drive-" + str(threadID)
        global logger
        global start
        start = Start
        logger = Logger
        logger.info("Robot | Code: DriveThread.py Init")
        

        
 
   



    def run(self):
        logger.info("Starting Drive Thread: " + self.name)
        global start
        while start:
            logger.info("Run Loop")
        else:
            logger.info("Stopping Drive Thread")
            return #Stop Drive Thread

    def stopDrive(self):
        global start
        start = False
            
        
