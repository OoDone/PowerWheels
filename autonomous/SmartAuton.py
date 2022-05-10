from drive.DriveControl import DriveControl
from Variables import Constants
from other.DistanceSensor import DistanceSensor
import asyncio
class SmartAuton:
    def __init__(self, Logger):
        global logger
        global drive
        global constants
        global distanceSensor
        constants = Constants()
        logger = Logger
        distanceSensor = DistanceSensor(logger)
        logger.info("Robot | Code: SmartAuton.py Init")
        drive = DriveControl(logger)

    def start(self):
        logger.info("Auton: Starting SmartAuton...")
        global start
        start = True
        self.loop()
        asyncio.run(self.initialize()) #Figure out positioning for this and loop function call

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
            if distanceSensor.getSonar() <= constants.AutonConstants().minDistance:
                logger.info("Auton: To close, Perform turn")
                drive.stopRobot()
                #asyncio.run(self.TURN ASYNC FUNCTION)
            logger.info("TEMP SMARTAUTON LOOP")

    def isFinished():
        return False

    
    async def avoidObsticle():
        steerPercent = 10 # Temp Calculate steer needed or get a constant
        drive.steerServoPerc(steerPercent)
        drive.driveDistAuton(constants.AutonConstants().turnDistance, constants.AutonConstants().avoidObsticleSpeed)
