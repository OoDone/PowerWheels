import os
from time import sleep
from Constants import Constants
try:
    import pigpio
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO

speed = 0.0
motor = False

class DriveMotor:
  def __init__(self, motorPin, Logger):
    global motor
    global logger
    global constants
    global pi
    motor = motorPin
    logger = Logger
    constants = Constants()
    GPIO.setmode(GPIO.BCM)
    if constants.isTestingMode == False:
      os.system("sudo pigpiod")
      sleep(1)
      pi = pigpio.pi()
      pi.set_servo_pulsewidth(motor, 0)
    logger.info("Robot | Code: DriveMotor.py Init.")
    
  def setMotorSpeed(self,speedPercent):
    speed = 0.0
    if speedPercent > 0:
      speed = constants.DriveConstants().motorNeutralSpeed+speedPercent*5
    else:
      speed = speedPercent*5+constants.DriveConstants().motorNeutralSpeed
    if constants.isTestingMode == False:
      pi.set_servo_pulsewidth(motor, speed)
    else: logger.info("TestMode: Set Motor Speed to " + str(speedPercent))
    
  def stopMotor(self):
    if constants.isTestingMode == False:
      pi.set_servo_pulsewidth(motor, 0.0)
    else: logger.info("TestMode: Stopping motor...")
    
  def getDriveSpeedPercent(self):
    return speed

#Getters for encoder ticks, motor speed
#Encoder logic
