from Logger import Logger
#import numpy.core.multiarray
from other.Vision import Vision
from time import sleep

#try:
logger = Logger("TestVision")
vision = Vision(logger)
sleep(0.1)
vision.startVision()
  
#except KeyboardInterrupt:
  #print("EXITING NOW")
  #data.toString()

#FIXME ADD ON INTERRUPT CRASH PROGRAM
