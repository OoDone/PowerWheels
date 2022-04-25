from time import sleep
from Constants import Constants
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO


class Buzzer:
  def __init__(self, Logger):
    logger.info("Robot | Code: Buzzer.py Init.")
    global logger
    global constants
    logger = Logger
    constants = Constants()
    GPIO.setup(constants.buzzerPin, GPIO.OUT)
    GPIO.output(constants.buzzerPin, GPIO.LOW)
  
  def buzz(length, amount):
    buzz=amount
    try:
      while (buzz > 0):
        if buzz > 0:
          logger.info("Buzzer Alert")
          GPIO.setmode(GPIO.BCM)
          GPIO.output(constants.buzzerPin,GPIO.HIGH)
          sleep(length)
          GPIO.output(constants.buzzerPin,GPIO.LOW)
          sleep(length)
          buzz = buzz-1
        else:
          break
    except:
      logger.warn("Robot: Exception in Buzz() function")
