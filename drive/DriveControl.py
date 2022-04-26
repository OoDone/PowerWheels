from drive.Motor import Motor
from Constants import Constants

class DriveControl:
  
  def __init__(self, Logger):
    global logger
    global constants
    global driveMotor
    logger = Logger
    logger.info("Robot | Code: DriveControl.py Init.")
    constants = Constants()
    driveMotor = Motor(constants.DriveConstants().ESC, logger)
  
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
    if direction < 0:
      directionPosition = -direction * constants.DriveConstants().directionTicksPer + constants.DriveConstants().servoNeutralPosition #* 9.36 + 1489 # TEMP  
    else:
      directionPosition = constants.DriveConstants().servoNeutralPosition - direction * constants.DriveConstants().directionTicksPer   # 1489 - direction * directionTicksPer #* 9.36        #1489 mid servo position
    #pi.set_servo_pulsewidth(servoPin, directionPosition)
    
    
  def stopRobot(self):
    driveMotor.stopMotor()
    
