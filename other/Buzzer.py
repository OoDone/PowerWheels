buzzerPin = 17

class Buzzer:
  GPIO.setup(buzzerPin, GPIO.OUT)
  GPIO.output(buzzerPin, GPIO.LOW)
  
  def buzz(length, amount):
    buzz=amount
    try:
      while (buzz > 0):
        if buzz > 0:
          logger.info("Buzzer Alert")
          GPIO.setmode(GPIO.BCM)
          GPIO.output(buzzerPin,GPIO.HIGH)
          sleep(length)
          GPIO.output(buzzerPin,GPIO.LOW)
          sleep(length)
          buzz = buzz-1
        else:
          break
