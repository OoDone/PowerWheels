#!/usr/bin/python

from DistanceSensor import DistanceSensor

class CollisionSensor:
  
  def __init__(self, socket, Logger):
    global logger
    global blsocket
    global distSensor
    logger = Logger
    distSensor = DistanceSensor(logger)
    logger.info("Robot | Code: CollisionSensor.py Init")
    blsocket = socket
  
  from threading import Thread
  def collisionWarning():
    while True:
      distance = distSensor.ultrasonicRead()
      if distance < 10:
        logger.info("Robot: Robot {} centimeters away from object!", distance)
        blsocket.send("cw")
      
  thread=Thread(target=collisionWarning)
  thread.start()
