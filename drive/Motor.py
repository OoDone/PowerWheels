import os
from time import sleep
from Variables import Constants
try:
    import pigpio
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO

speed = 0.0
motor = False

class Motor:
  def __init__(self, motorPin, Logger):
    global motor
    global logger
    global constants
    global pi
    motor = motorPin
    logger = Logger
    logger.info("Robot | Code: Motor.py Init.")
    constants = Constants()
    GPIO.setmode(GPIO.BCM)
    if constants.isTestingMode == False:
      os.system("sudo pigpiod")
      sleep(1)
      pi = pigpio.pi()
      pi.set_servo_pulsewidth(motor, 0)
    
  def setMotorSpeed(self,Speed):
    if not Speed > constants.DriveConstants().motorMaxSpeed and not Speed < constants.DriveConstants().motorMinSpeed:
      if constants.isTestingMode == False:
        pi.set_servo_pulsewidth(motor, speed)
      else: logger.info("TestMode: Set Motor Speed to " + str(Speed))
    else: logger.info("setMotorSpeed: Speed not within allowed speed range.")

  def setMotorSpeedPercent(self,speedPercent):
    if speedPercent > -101 and speedPercent < 101:
      speed = 0.0
      if speedPercent > 0:
        speed = constants.DriveConstants().motorNeutralSpeed+speedPercent*5
      else:
        speed = speedPercent*5+constants.DriveConstants().motorNeutralSpeed
      if constants.isTestingMode == False:
        pi.set_servo_pulsewidth(motor, speed)
      else: logger.info("TestMode: Set Motor Speed to " + str(speedPercent) + " Percent.")
    else: logger.info("setMotorSpeedPercent: SpeedPercent not within allowed speed range.")
    
  def stopMotor(self):
    if constants.isTestingMode == False:
      pi.set_servo_pulsewidth(motor, 0.0)
    else: logger.info("TestMode: Stopping motor...")
    
  def getMotorSpeed(self):
    return speed

#Getters for encoder ticks, motor speed
#Encoder logic
