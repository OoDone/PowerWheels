from DriveMotor import DriveMotor
from Constants import Constants

class DriveControl:
  
  def __init__(self, Logger):
    global logger
    global constants
    global driveMotor
    logger = Logger
    constants = Constants(logger)
    driveMotor = DriveMotor(constants.ESC, logger)

    logger.info("Robot | Code: DriveControl.py Init.")
  
  def driveRobot(x):
    speed = x.decode('UTF-8').split(':')[2].replace("'",'')
    direction = x.decode('UTF-8').split(':')[4].replace("'",'')
    try:
      speed = float(speed)
      direction = float(direction)
    except:
      speed = 0.0
      direction = 0.0
      logger.warn("Exception: speed or direction not a number")
    if speed > 0:#0
      driveMotor.setMotorSpeed(speed*5+constants.motorNeutralSpeed)
    elif speed < 0: #0
      driveMotor.setMotorSpeed(constants.motorNeutralSpeed + speed * 5)
    else:
      driveMotor.setMotorSpeed(0)
    if direction < 0:
      directionPosition = -direction * constants.directionTicksPer + constants.servoNeutralPosition #* 9.36 + 1489 # TEMP  
    else:
      directionPosition = constants.servoNeutralPosition - direction * constants.directionTicksPer   # 1489 - direction * directionTicksPer #* 9.36        #1489 mid servo position
    #pi.set_servo_pulsewidth(servoPin, directionPosition)
    
    
  def stopRobot():
    driveMotor.stopMotor()
    
