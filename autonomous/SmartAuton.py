from drive.DriveControl import DriveControl
from Variables import Constants
import asyncio
class SmartAuton:
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
        self.loop()
        asyncio.run(self.initialize())

    def stop(self):
        global start
        logger.info("Disabling SmartAuton.")
        start = False

    async def initialize(self):
        #OPTIONAL, RUNS ONCE AT START AND IS ASYNC
        logger.info("AUTON INITIALIZE")
        drive.driveOpenLoop(constants.AutonConstants().openLoopSpeed)

    def loop(self):
        while start:
            
            logger.info("TEMP SMARTAUTON LOOP")
