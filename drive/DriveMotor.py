import sys
sys.path.append('/home/Desktop/PowerWheels/')
from ..Constants import Constants
from Logger import Logger
speed = 0.0
constants = Constants()
motor = False
logger = Logger("DriveMotor") #Make it specific for each motor?

class DriveMotor:
  
  def __init__(motorPin):
    motor = motorPin
    
  def driveMotor(speedPercent):
    speed = 0.0
    if speedPercent > 0:
      speed = motorNeutralSpeed+speedPercent*5
    else:
      speed = speedPercent*5+motorNeutralSpeed
    pi.set_servo_pulsewidth(motor, speed)
    
  def stopMotor():
    pi.set_servo_pulsewidth(motor, 0.0)
    
  def getDriveSpeedPercent():
    return speed

#Getters for encoder ticks, motor speed
#Encoder logic
