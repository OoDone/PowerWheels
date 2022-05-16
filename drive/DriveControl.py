from drive.Motor import Motor
from drive.Servo import Servo
from Variables import Constants

class DriveControl:
  
  def __init__(self, Logger):
    global logger
    global constants
    global driveMotor
    global steerServo
    logger = Logger
    logger.info("Robot | Code: DriveControl.py Init.")
    constants = Constants()
    driveMotor = Motor(constants.DriveConstants().motorPin, logger)
    steerServo = Servo(constants.DriveConstants().servoPin, logger)
  
  def driveRobot(self, x):
    speed = x.decode('UTF-8').split(':')[2].replace("'",'')
    direction = x.decode('UTF-8').split(':')[4].replace("'",'')
    #TESTMODE FAKE BYTE:   0:1:10:3:0
    try:
      speed = float(speed)
      direction = float(direction)
    except:
      speed = 0.0
      direction = 0.0
      logger.warn("Exception: speed or direction not a number")
    if speed > 0:#0
      driveMotor.setMotorSpeed(speed*5+constants.DriveConstants().motorNeutralSpeed)
    elif speed < 0: #0
      driveMotor.setMotorSpeed(constants.DriveConstants().motorNeutralSpeed + speed * 5)
    else:
      driveMotor.setMotorSpeed(0)
    if direction > 0:
      steerServo.setServoPosition(-direction * constants.DriveConstants().directionTicksPer + constants.DriveConstants().servoNeutralPosition) #* 9.36 + 1489 # TEMP
      #logger.info("STEERSERVO: " + str(direction * constants.DriveConstants().directionTicksPer + constants.DriveConstants().servoNeutralPosition))
    else:
      steerServo.setServoPosition(-direction * constants.DriveConstants().directionTicksPer + constants.DriveConstants().servoNeutralPosition)   # 1489 - direction * directionTicksPer #* 9.36        #1489 mid servo position
      #logger.info("STEERSERVO: " + str(constants.DriveConstants().servoNeutralPosition + direction * constants.DriveConstants().directionTicksPer))
    
  async def driveDistAuton(self, distance, speedPercent):
    #AWAIT UNTIL DISTANCETICKS(ADDED UP MOTOR TICKS) EQUALS DISTANCE
    global stop
    stop = False
    distanceTicks = distance * constants.DriveConstants().driveTicksPerMeter
    logger.info("Driving " + str(distance) + " meters at " + str(speedPercent) + " percent speed.")
    driveMotor.setMotorSpeedPercent(speedPercent)
    distanceDriven = 0
    while not driveMotor.getEncoderTicks() == distanceTicks:
      distanceDriven +=1 #FIXME MAKE GLOBAL VARIABLE AND GETTER FUNCTION
      if stop:
        return 
      else: 
        driveMotor.setEncoderTicks(driveMotor.getEncoderTicks() + 1)
        if driveMotor.getEncoderTicks() == distanceTicks:
          return
    #Real Encoder  Logic
    #isSame = True
    #while not distanceDriven == distanceTicks:
      #if driveMotor.getEncoderTicks() == 0 and not isSame:
        #isSame =True
        #distanceDriven += constants.DriveConstants().maxEncoderTicks
      #elif not driveMotor.getEncoderTicks() == 0 and isSame:
        #isSame = False



  def stopDriveDistAuton(self):
    global stop
    stop = True
    logger.info("DriveDistAuton: Stopping Robot...")

  def driveOpenLoop(self, speedPercent):
    driveMotor.setMotorSpeedPercent(speedPercent)
    logger.info("Open Loop Driving Robot at {} Percent Speed", str(speedPercent))
    
  def steerServoPerc(self, steerPercent):
    steerServo.setServoPositionPercent(steerPercent)
    
    
  def stopRobot(self):
    driveMotor.stopMotor()
    steerServo.stopServo()
    global stop
    stop = True

  def getEncoderTicks(self):
    return driveMotor.getMotorSpeed()
    
