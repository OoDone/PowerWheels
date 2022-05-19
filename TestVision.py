from Logger import Logger
from Vision import Vision

try:
  logger = Logger("TestVision")
  vision = Vision(logger)
  vision.start()
  
except KeyboardInterrupt:
  disableRobot()
  print("EXITING NOW")
  j.quit()
  data.toString()

#FIXME ADD ON INTERRUPT CRASH PROGRAM
