#!/usr/bin/python

from drive.DriveControl import DriveControl
from Variables import Constants
from other.DistanceSensor import DistanceSensor
from other import Vision
from multiprocessing import Process
from threading import Thread
import threading
from time import sleep
from autonomous.DriveThread import DriveThread
import asyncio
from client.timer import Timer
class SmartAuton:
    global isAvoiding
    global prevTicksDistance
    isAvoiding = False
    prevTicksDistance = 0
    def __init__(self, Logger):
        global logger
        global drive
        global constants
        constants = Constants()
        logger = Logger
        logger.info("Robot | Code: SmartAuton.py Init")
        drive = DriveControl(logger)

    def start(self):
        logger.info("Auton: Starting SmartAuton...")
        global start
        start = True
        self.visionThread = Vision.Vision(logger, 1, start) #Creates New Vision Thread #FIXME
        self.visionThread.start() #FIXME
        self.driveThread=DriveThread(logger, 1, drive, start) #Figure out positioning for this and loop function call
        self.driveThread.start()
        #CHECK IF ALL THREAD IDS CAN BE 1 FIXME
        self.loopThread=LoopThread(logger, 1, drive, self.visionThread, self.driveThread, start) 
        self.loopThread.start() #FIXME


    def stop(self):
        global start
        start = False
        self.loopThread.join()
        self.visionThread.stopVision()
        self.visionThread.join()
        self.driveThread.stopThread()
        self.driveThread.join()
        self.loopThread.stopThread()
        self.loopThread.join()
        logger.info("Disabled SmartAuton.")
        drive.stopRobot()


    def isFinished(self):
        return False

    
    async def avoidObsticle(self):
        global isAvoiding
        global prevTicksDistance
        prevTicksDistance = drive.getEncoderTicks()
        isAvoiding = True
        steerPercent = 10 # Temp Calculate steer needed or get a constant
        drive.steerServoPerc(steerPercent)
        drive.driveDistAuton(constants.AutonConstants().turnDistance, constants.AutonConstants().avoidObsticleSpeed)

    def reverseAvoid(self):
        global prevTicksDistance
        drive.steerServoPerc(10)# Same value as above
        drive.driveDistAuton(constants.AutonConstants().turnDistance, constants.AutonConstants().avoidObsticleSpeed)

    
class LoopThread(threading.Thread):

    def __init__(self, Logger, threadID, Drive, Vision, DriveThread, Start):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "Loop-" + str(threadID)
        global logger
        global drive
        global start
        global constants
        global driveThread
        global vision
        global distanceSensor
        driveThread = DriveThread
        vision = Vision
        start = Start
        drive = Drive
        logger = Logger
        constants = Constants()
        distanceSensor = DistanceSensor(logger)
        logger.info("Robot | Code: SmartAuton.LoopThread Init")

    
    def run(self):
        logger.info("Started Loop Thread!")
        global start
        stop = False
        timer = Timer()
        isAvoiding = False
        while start:
            #logger.info("DISTANCESENSOR: " + str(distanceSensor.getSonar()))
            if timer.hasStarted() and timer.hasElapsed(2):
                logger.info("Done Backing Up!")
                timer.reset()
                timer.stop()
                driveThread.driveRobot(False)
                stop = False
                isAvoiding = False
            if distanceSensor.getSonar() <= constants.AutonConstants().minDistance and not isAvoiding:  #FIXME OPPOSITE <> SIGN
                logger.info("Auton: To close, Perform turn")
                #drive.stopRobot()
                #driveThread.stopRobot()
                driveThread.driveRobot(True)
                isAvoiding = True
                if not timer.hasStarted():
                    timer.start()
                stop = True
                #IF not using vision to avoid do below
                drive.steerServoPerc(50) #steer left 
                #FIXME Add turn direction so it doesnt go back into the object it just backed up for
            elif distanceSensor.getSonar() <= constants.AutonConstants().avoidMinDistance and 1==2:#isAvoiding:
                logger.info("Auton: Distance to close while avoiding obsticle, fallback to reverse avoid")
                #drive.stopRobot()
                driveThread.stopRobot()
                isAvoiding = False
                #Fall back to reverse here
            elif isAvoiding:
                drive.driveOpenLoopNL(constants.AutonConstants().openLoopSpeed)
            if vision.getLastDirection() == 0 and not stop:
                #Forward
                drive.steerServoPerc(0)
                #logger.info("Forwards")
            elif vision.getLastDirection() == 1 and not stop:
                #backwards
                drive.steerServoPerc(0)
                #logger.info("Backwards")
            elif vision.getLastDirection() == 2 and not stop:
                #right
                drive.steerServoPerc(-100)
            elif vision.getLastDirection() == 3 and not stop:
                #left
                drive.steerServoPerc(50)
            elif vision.getLastDirection() == 4 and not stop:
                #stop
                driveThread.stopRobot()
            elif vision.getLastDirection() == 5:
                #Not Set Yet
                x=1
                #logger.info("No Vision Setting Yet")
        if not start:
            logger.info("Stopping Loop Thread")
            return

    def stopThread(self):
        global start
        start = False

