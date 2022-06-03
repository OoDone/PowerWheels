#!/usr/bin/python

from time import sleep
from Variables import Constants
from drive.DriveControl import DriveControl
import asyncio

isAutonFinished = False
class DriveForwardAuton:
    def __init__(self, Logger):
        global logger
        global driveMotor
        logger = Logger
        logger.info("Robot | Code: DriveForwardAuton.py Init")
        driveMotor = DriveControl(Logger)

    def start(self):
        logger.info("Auton: Starting DriveForwardAuton...")
        global start
        start = True
        asyncio.run(self.initialize())

    async def initialize(self):
        global isAutonFinished
        global start
        logger.info("AUTON INITIALIZE")
        await driveMotor.driveDistAuton(5, 100)
        if start:
            start = False
            logger.info("Drive Distance Finished!")
        isAutonFinished = True
        
    def stop(self):
        global start
        start = False
        driveMotor.stopDriveDistAuton()
        logger.info("Force Stopping DriveForwardAuton")
        
    def isFinished(self):
        return isAutonFinished

