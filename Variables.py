#Example use:     constants.DriveConstants().ESC
class Constants:

  isTestingMode = False #Bypasses Need to be ran on Pi, disables bluetooth server, ETC

  #robot constants
  ultrasonicSensorEnabled = False
  buzzer = True
  buzzerPin=17

  #Robot Constants
  class RobotConstants:
    wheelBaseMeters = 2 #FIXME Wheelbase for Autonomous/Automated calculations IN METERS WB 
    maxSteerAngle = 10 #FIXME Check steering angle, not 10
    minTurnRadius = 1 #FIXME 
    #Turning radius calculation: TR = WB/tan(a)

  #Drive constants
  class DriveConstants:
    #Drive Motors
    motorPin = 4
    motorNeutralSpeed = 1500
    motorMinSpeed = 1000
    motorMaxSpeed = 2000

    #Steering Servos
    servoPin = 18
    servoNeutralPosition = 1488 #1488 for 556-2420 & 1700 for 1500-1900
    directionTicksPer = 9 #2
    servoMaxLimitTicks = 2388 #1900
    servoMinLimitTicks = 588 #1500

    #Encoder 
    driveTicksPerMeter = 10000


  #Auton Constants
  class AutonConstants:
    autonMode = 1
    autonEnabled = False
    openLoopSpeed = 20 #Auton Open Loop Drive Speed Percent
    minDistance = 10 #Min distance to be within to turn away : IN CENTIMETERS
    turnDistance = 10 #FIXME The distance to drive in autonomous while turning to avoid obstacle
    avoidObsticleSpeed = 20 #Percent speed of car while turning to avoid obstacle

  #Bluetooth Constants
  class BluetoothConstants:
    bd_addr = ""#"DC:A6:32:6B:38:BD"  #"B8:27:EB:D6:57:CE" 
    #B8:27:EB:6B:AB:4B
    uuid = "42b58f76-b26d-11ea-b733-cb205305bc99"
    port = 1


# Variables, Objects that change state
class Variables:
    class DriveVariables:
      example = 2



