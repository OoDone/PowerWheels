import sys
sys.path.append('/home/Desktop/PowerWheels/')
from ..Constants import Constants 
speed = 0.0
constants = Constants()
motor = False

class DriveMotor:
  
  def __init__(motorPin):
    motor = motorPin
    
  def driveMotor(speedPercent):
    speed = 0.0
    if speedPercent > 0:
      speed = motorNeutralSpeed+speedPercent*5
    else:
      speed = speedPercent*5+motorNeutralSpeed
    driveSpeed = speed
    pi.set_servo_pulsewidth(motor, speed)

#Getters for encoder ticks, motor speed
#Encoder logic
