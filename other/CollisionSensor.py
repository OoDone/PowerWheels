from sensor import ultrasonicRead

class CollisionSensor:
  
  def __init__(self, socket, Logger):
    global logger
    global blsocket
    logger = Logger
    logger.info("Robot | Code: CollisionSensor.py Init")
    blsocket = socket
  
  from threading import Thread
  def collisionWarning():
    while True:
      distance = ultrasonicRead()
      if distance < 10:
        logger.info("Robot: Robot {} centimeters away from object!", distance)
        blsocket.send("cw")
      
  thread=Thread(target=collisionWarning)
  thread.start()
