import Constants
speed = 0.0
constants = Constants()

class DriveMotor:
  def driveMotor(speedPercent):
    speed = 0.0
    if speedPercent > 0:
      speed = motorNeutralSpeed+speedPercent*5
    else:
      speed = speedPercent*5+motorNeutralSpeed
    driveSpeed = speed
    pi.set_servo_pulsewidth(ESC, speed)
