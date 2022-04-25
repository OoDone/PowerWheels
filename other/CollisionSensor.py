from sensor import ultrasonicRead

class CollisionSensor:
  
  def __init__(self, socket, Logger):
    logger.info("Robot | Code: CollisionSensor.py Init")
    global logger
    global blsocket
    logger = Logger
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
