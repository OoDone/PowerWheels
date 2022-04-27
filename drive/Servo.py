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

position = 0.0
servo = False

class Servo:
  def __init__(self, motorPin, Logger):
    global servo
    global logger
    global constants
    global pi
    logger = Logger
    logger.info("Robot | Code: Motor.py Init.")
    constants = Constants()
    servo = constants.DriveConstants().servoPin
    GPIO.setmode(GPIO.BCM)
    if constants.isTestingMode == False:
      os.system("sudo pigpiod")
      sleep(1)
      pi = pigpio.pi()
      pi.set_servo_pulsewidth(servo, 0)
    
  def setServoPosition(self,Position):
    if not Position > constants.DriveConstants().servoMaxLimitTicks and not Position < constants.DriveConstants().servoMinLimitTicks:
      if constants.isTestingMode == False:
        pi.set_servo_pulsewidth(servo, Position)
      else: logger.info("TestMode: Set Servo Position to " + str(Position))
    else: logger.info("setServoPosition: Speed not within allowed position range.")

  def setServoPositionPercent(self,positionPercent):
    if positionPercent > -101 and positionPercent < 101:
      position = 0.0
      if positionPercent > 0:
        position = constants.DriveConstants().motorNeutralSpeed+positionPercent*5
      else:
        position = positionPercent*5+constants.DriveConstants().motorNeutralSpeed
      if constants.isTestingMode == False:
        pi.set_servo_pulsewidth(servo, position)
      else: logger.info("TestMode: Set Servo Position to " + str(positionPercent))
    else: logger.info("setServoPositionPercent: positionPercent not within allowed position range.")
    
  def stopMotor(self):
    if constants.isTestingMode == False:
      pi.set_servo_pulsewidth(motor, 0.0)
    else: logger.info("TestMode: Stopping motor...")
    
  def getDriveSpeedPercent(self):
    return speed

#Getters for encoder ticks, motor speed
#Encoder logic

