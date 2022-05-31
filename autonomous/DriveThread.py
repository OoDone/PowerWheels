#!/usr/bin/python

import os
import threading
from Variables import Constants


start = False
stop = False
driveDirection = "F"
class DriveThread(threading.Thread):
    def __init__(self, Logger, threadID, Drive, Start):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "Drive-" + str(threadID)
        global logger
        global drive
        global start
        global constants
        start = Start
        drive = Drive
        logger = Logger
        constants = Constants()
        logger.info("Robot | Code: DriveThread.py Init")
        

        
    def run(self):
        logger.info("Starting Drive Thread: " + self.name)
        global start
        global driveDirection
        while start:
            if not stop:
                if driveDirection  == "N":
                    #No direction yet
                    x=1
                elif driveDirection  == "F":
                    #Forwards
                    drive.driveOpenLoopNL(constants.AutonConstants().openLoopSpeed)
                elif driveDirection  == "B":
                    #Backwards
                    logger.info("Backwards")
                    drive.driveOpenLoopNL(-constants.AutonConstants().openLoopSpeed)
            else:
                drive.stopRobot()
        else:
            logger.info("Stopping Drive Thread")
            return #Stop Drive Thread

    def stopThread(self):
        global start
        start = False


    def stopRobot(self):
        global stop
        stop = True
        logger.info("DriveThread: Stopping robot..")

    def driveRobot(self,isReverse):
        #if isReverse is true, drive backwards, else drive forwards
        global driveDirection
        global stop
        stop = False
        if isReverse:
            driveDirection = "B"
            logger.info("DriveThread: Driving Robot Backwards...")
        else:
            driveDirection = "F"
            logger.info("DriveThread: Driving Robot Forwards...")

    def getDriveDirection(self):
        return driveDirection

            
        
