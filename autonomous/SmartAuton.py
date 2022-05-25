#!/usr/bin/python

from drive.DriveControl import DriveControl
from Variables import Constants
from other.DistanceSensor import DistanceSensor
from other import Vision
from multiprocessing import Process
from threading import Thread
from time import sleep
import asyncio
class SmartAuton:
    global isAvoiding
    global prevTicksDistance
    isAvoiding = False
    prevTicksDistance = 0
    def __init__(self, Logger):
        global logger
        global drive
        global constants
        global distanceSensor
        constants = Constants()
        logger = Logger
        distanceSensor = DistanceSensor(logger)
        #vision = Vision.Vision(logger)
        #vision = Vision.Vision(logger, "Vision-1")
        logger.info("Robot | Code: SmartAuton.py Init")
        drive = DriveControl(logger)

    def start(self):
        logger.info("Auton: Starting SmartAuton...")
        global start
        global threadD
        global thread
        global visionT #FIXME
        start = True
        visionT = Vision.Vision(logger, 1, start) #Creates New Vision Thread #FIXME
        visionT.start() #FIXME
        threadD=Thread(asyncio.run(self.initialize(drive))) #Figure out positioning for this and loop function call
        threadD.start()
        thread=Thread(target=self.loop, args=(logger, drive, visionT))#, vision)) 
        thread.start() #FIXME

        #logger.info("After Start Vision") #FIXME

    def stop(self):
        global start
        global thread
        global visionT
        start = False
        thread.join()
        visionT.stopVision()
        visionT.join()
        logger.info("Disabled SmartAuton.")
        drive.stopRobot()

    async def initialize(self, drive2):
        #OPTIONAL, RUNS ONCE AT START AND IS ASYNC
        drive2.driveOpenLoop(constants.AutonConstants().openLoopSpeed)

    def loop(self, logger, drive, vision):
        global isAvoiding
        logger.info("Started Loop Thread!")
        #vision = Vision.Vision(logger)#FIXME
        global start
        while start:
            #vision.startVision()#FIXME
            if distanceSensor.getSonar() <= constants.AutonConstants().minDistance and not isAvoiding:  #FIXME OPPOSITE <> SIGN
                logger.info("Auton: To close, Perform turn")
                drive.stopRobot()
                #asyncio.run(self.TURN ASYNC FUNCTION)
            elif distanceSensor.getSonar() <= constants.AutonConstants().avoidMinDistance and isAvoiding:
                logger.info("Auton: Distance to close while avoiding obsticle, fallback to reverse avoid")
                drive.stopRobot()
                isAvoiding = False
                drive.stopDriveDistAuton()
                #Fall back to reverse here
            if vision.getLastDirection() == 0:
                #Forward
                drive.steerServoPerc(0)
                logger.info("Forwards")
            elif vision.getLastDirection() == 1:
                #backwards
                drive.steerServoPerc(0)
                logger.info("Backwards")
            elif vision.getLastDirection() == 2:
                #right
                drive.steerServoPerc(50)
            elif vision.getLastDirection() == 3:
                #left
                drive.steerServoPerc(-50)
            elif vision.getLastDirection() == 4:
                #stop
                drive.stopRobot()
            elif vision.getLastDirection() == 5:
                #Not Set Yet
                logger.info("No Vision Setting Yet")
        if not start:
            logger.info("Stopping Loop Thread")
            return


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

