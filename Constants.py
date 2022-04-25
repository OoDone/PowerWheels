#Example use:     constants.DriveConstants().ESC
class Constants:
  def __init__(self, Logger):
      Logger.info("Robot | Code: Constants.py Init.")

  isOnRobot = False

  #robot constants
  enabled = False
  disconnected = False
  ultrasonicSensorEnabled = False
  buzzer = False
  buzzerPin=17
  temp1=1
  #Drive constants
  class DriveConstants:
    motorNeutralSpeed = 1500
    motorMinSpeed = 1000
    motorMaxSpeed = 2000
    servoPin = 18
    ESC = 4
    servoNeutralPosition = 1700 #1488 for 556-2420 & 1700 for 1500-1900
    directionTicksPer = 2 #(Ticks of rotation)/100 #100 is for input value

  #Auton Constants
  class AutonConstants:
    autonMode = 1
    autonEnabled = False
  
  #Bluetooth Constants
  class BluetoothConstants:
    bd_addr = "DC:A6:32:6B:38:BD"  #"B8:27:EB:D6:57:CE" 
    #B8:27:EB:6B:AB:4B
    uuid = "42b58f76-b26d-11ea-b733-cb205305bc99"
    port = 1



