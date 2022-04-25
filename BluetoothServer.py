import bluetooth
from Constants import Constants
#logger = Logger("robotLog")
connected = False
class BluetoothServer:
  def __init__(self, Logger):
    global logger
    global constants
    logger = Logger
    constants = Constants()
    logger.info("Robot | Code: BluetoothServer.py Initialized.")
    if constants.isTestingMode == False:
      self.StartServer()

  def StartServer():
    global connected
    global server_socket
    global client_socket
    server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    server_socket.bind((constants.BluetoothConstants().bd_addr, bluetooth.PORT_ANY)) #bluetooth.PORT_ANY
    server_socket.listen(constants.BluetoothConstants().port)
    logger.info("Bluetooth Bind: Listening on port " + str(constants.BluetoothConstants().port))
    #enabledAlert(0.1, 3)
    bluetooth.advertise_service(server_socket, "SampleServer", service_classes=[bluetooth.SERIAL_PORT_CLASS],profiles=[bluetooth.SERIAL_PORT_PROFILE])
    logger.info("Bluetooth: Advertising Service!")


    client_socket, address = server_socket.accept
    logger.info("Bluetooth: Accepting client!")
    logger.info("Bluetooth: Device connected!")
    client_socket.send("connected") #ADD CODE TO HANDLE ON CLIENT SIDE
    connected = True
  #enabledAlert(0.2, 2) #2 bluetooth connected 
    
  def return_data(self):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            #print(data) #PRINT LINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
            return data
    except OSError:
        pass
  
  def getServerSocket(self):
    if server_socket != None:
      return server_socket

  def getStatus(self):
    return connected
