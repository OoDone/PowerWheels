#!/usr/bin/python

import os
import threading
from Variables import Constants


start = False
stop = False
driveDirection = "N"
class DriveThread(threading.Thread):
    def __init__(self, Logger, threadID, Drive, Start):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "Drive-" + str(threadID)
        global logger
        self.start = Start
        self.drive = Drive
        logger = Logger
        self.constants = Constants()
        logger.info("Robot | Code: DriveThread.py Init")
        

        
    def run(self):
        logger.info("Starting Drive Thread: " + self.name)
        while self.start:
            if not stop:
                if driveDirection  == "N":
                    #No direction yet
                    x=1
                elif driveDirection  == "F":
                    #Forwards
                    self.drive.driveOpenLoop(self.constants.AutonConstants().openLoopSpeed)
                elif driveDirection  == "B":
                    #Backwards
                    self.drive.driveOpenLoop(-self.constants.AutonConstants().openLoopSpeed)
            else:
                self.drive.stopRobot()
        else:
            logger.info("Stopping Drive Thread")
            return #Stop Drive Thread

    def stopThread(self):
        self.start = False
        logger.info("DriveThread: Stopping Thread...")


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
        else:
            driveDirection = "F"
        logger.info("DriveThread: Driving Robot...")

    def getDriveDirection(self):
        return driveDirection

            
        
