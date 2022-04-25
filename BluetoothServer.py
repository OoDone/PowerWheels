import bluetooth
from Constants import Constants
#logger = Logger("robotLog")

class BluetoothServer:
  connected = False

  def __init__(self, Logger):
    global logger
    global constants
    logger = Logger
    constants = Constants(logger)
    logger.info("Robot | Code: BluetoothServer.py Init.")


    
  global server_socket
  global client_socket
  server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  server_socket.bind((constants.BluetoothConstants().bd_addr, bluetooth.PORT_ANY))
  server_socket.listen(constants.BluetoothConstants().port)
  logger.info("Bluetooth Bind: Listening on port " + str(constants.BluetoothConstants().port))
  #enabledAlert(0.1, 3)
  bluetooth.advertise_service(server_socket, "SampleServer", service_classes=[bluetooth.SERIAL_PORT_CLASS],profiles=[bluetooth.SERIAL_PORT_PROFILE])
  logger.info("Bluetooth: Advertising Service!")


  client_socket, address = server_socket.accept()
  logger.info("Bluetooth: Accepting client!")
  logger.info("Bluetooth: Device connected!")
  client_socket.send("connected") #ADD CODE TO HANDLE ON CLIENT SIDE
  connected = True
  #enabledAlert(0.2, 2) #2 bluetooth connected 
    
  def return_data():
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            #print(data) #PRINT LINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
            return data
    except OSError:
        pass
  
  def getServerSocket():
    if server_socket != None:
      return server_socket
