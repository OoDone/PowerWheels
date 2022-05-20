from drive.DriveControl import DriveControl
from Variables import Constants
from other.DistanceSensor import DistanceSensor
from other.Vision import Vision
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
        global vision
        constants = Constants()
        logger = Logger
        distanceSensor = DistanceSensor(logger)
        vision = Vision(logger)
        logger.info("Robot | Code: SmartAuton.py Init")
        drive = DriveControl(logger)

    def start(self):
        logger.info("Auton: Starting SmartAuton...")
        global start
        start = True
        self.loop()
        self.vision.startVision() #DOESNT RUN BECAUSE OF ABOVE LOOP CALL
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
        global isAvoiding
        while start:
            if distanceSensor.getSonar() <= constants.AutonConstants().minDistance and not isAvoiding:
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

