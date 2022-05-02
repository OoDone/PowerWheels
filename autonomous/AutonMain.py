from Variables import Constants
from time import sleep
from autonomous.DriveForwardAuton import DriveForwardAuton

autonEnabled = False
class AutonMain:
    autonMode = 0
    def __init__(self, Logger):
        global logger
        global constants
        logger = Logger
        logger.info("Robot | Code: AutonMain.py Init")
        constants = Constants()

    
    def setSocket(self, Sock):
        global sock
        sock = Sock
        logger.info("Set Socket!")

    def setAutonMode(self, mode):
        global autonMode
        if autonEnabled == False:
            try:
                mode = int(mode)
            except:
                logger.warn("Robot | setAutonMode: Not a valid Number, defaulting to mode 0")
                mode = 0
            autonMode = mode
            logger.info("Robot | Set Autonomous Mode to " + str(mode))
        else:
            logger.info("Robot | Cannot Change AutonMode While Autonomous Mode Is Enabled.")

    def enableAuton(self, enabled):
        global autonEnabled
        if autonEnabled == True and enabled == True:
            logger.info("Robot | Autonomous Already Enabled.")
        elif autonEnabled == False and enabled == False:
            logger.info("Robot | Autonomous Already Disabled.")
        elif enabled == True:
            #AUTON ENABLED
            autonEnabled = enabled
            logger.info("Robot | Enabling Autonomous In Mode " + str(autonMode))
            sock.send("auton,enable")
            self.auton()
        else:
            #AUTON DISABLED
            autonEnabled = enabled
            logger.info("Robot | Disabling Autonomous Mode.")
            sock.send("auton,disable")


    def auton(self):
        global auton
        if autonMode == 0:
            #autonMode 0
            auton = DriveForwardAuton(logger)
            auton.start()
            self.loop()
        elif autonMode == 1:
            #autonMode 1
            logger.info("TEMP: REMOVE THIS IN AUTON ENABLED LOOP: AUTONMODE = 1")
            #CircleAuton().start() #Drives in circles #MAKE EACH AUTON IN A DIFFERENT FILE AND CLASS
        else: logger.info("Auton(): Autonomous Mode Not Enabled")
        
        
    def loop(self):
        while autonEnabled:
            if auton.isFinished():
                self.enableAuton(False)
            
    


