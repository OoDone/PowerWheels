import pigpio
import os
import RPi.GPIO as GPIO
from time import sleep
from Constants import Constants
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
    constants = Constants(logger)
    
    GPIO.setmode(GPIO.BCM)
    os.system("sudo pigpiod")
    sleep(1)
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(motor, 0)
    
  def setMotorSpeed(speedPercent):
    speed = 0.0
    if speedPercent > 0:
      speed = constants.motorNeutralSpeed+speedPercent*5
    else:
      speed = speedPercent*5+constants.motorNeutralSpeed
    pi.set_servo_pulsewidth(motor, speed)
    
  def stopMotor():
    pi.set_servo_pulsewidth(motor, 0.0)
    
  def getDriveSpeedPercent():
    return speed

#Getters for encoder ticks, motor speed
#Encoder logic
