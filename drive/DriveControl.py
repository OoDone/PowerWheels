import DriveMotor
from ..Logger import Logger

ESC = 4

class DriveControl:
  logger = Logger("robotLog")
  driveMotor = DriveMotor(ESC)
  
  def __init__():
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
      driveMotor.driveMotor(speed*5+motorNeutralSpeed)
    elif speed < 0: #0
      driveMotor.driveMotor(motorNeutralSpeed + speed * 5)
    else:
      driveMotor.driveMotor(0)
    if direction < 0:
      directionPosition = -direction * directionTicksPer + servoNeutralPosition #* 9.36 + 1489 # TEMP  
    else:
      directionPosition = servoNeutralPosition - direction * directionTicksPer   # 1489 - direction * directionTicksPer #* 9.36        #1489 mid servo position
    #pi.set_servo_pulsewidth(servoPin, directionPosition)
    
    
  def stopRobot():
    driveMotor.stopMotor()
    
