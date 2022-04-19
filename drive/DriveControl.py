import DriveMotor

ESC = 4

class DriveControl:
  
  #def __init__():
  
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
      pi.set_servo_pulsewidth(ESC, speed*5+motorNeutralSpeed)
    elif speed < 0: #0
      pi.set_servo_pulsewidth(ESC, motorNeutralSpeed + speed * 5)
    else:
      pi.set_servo_pulsewidth(ESC, 0)
    if direction < 0:
      directionPosition = -direction * directionTicksPer + servoNeutralPosition #* 9.36 + 1489 # TEMP  
    else:
      directionPosition = servoNeutralPosition - direction * directionTicksPer   # 1489 - direction * directionTicksPer #* 9.36        #1489 mid servo position
    pi.set_servo_pulsewidth(servoPin, directionPosition)
                #Set servo To directionPosition
