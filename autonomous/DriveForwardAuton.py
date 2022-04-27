from time import sleep
from Constants import Constants
from drive.DriveControl import DriveControl
import asyncio

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
        #OPTIONAL, RUNS ONCE AT START AND IS ASYNC
        logger.info("AUTON INITIALIZE")
        await driveMotor.driveDistAuton(5, 100)
        logger.info("Drive Distance Finished!")

    #def loop(self):
        #runs every 20 milliseconds
       # logger.info("TEMP AUTON DRIVEFORWARDAUTON LOOP")

    #while(start):
        #sleep(0.02)
       # loop()
