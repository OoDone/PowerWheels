#!/usr/bin/python

from Variables import Constants
from time import sleep
from autonomous.DriveForwardAuton import DriveForwardAuton
from autonomous.SmartAuton import SmartAuton

global autonEnabled
autonEnabled = False
class AutonMain:
    autonMode = 0
    def __init__(self, Logger):
        global logger
        global constants
        logger = Logger
        logger.info("Robot | Code: AutonMain.py Init")
        constants = Constants()

    

    def setAutonMode(self, mode):
        global autonMode
        global autonEnabled
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
        elif enabled == True: #AUTON ENABLED
            autonEnabled = enabled
            logger.info("Robot | Enabling Autonomous In Mode " + str(autonMode))
            self.auton()
        else: #AUTON DISABLED
            autonEnabled = enabled
            logger.info("Robot | Disabling Autonomous Mode.")
            global auton
            auton.stop()


    def auton(self):
        global auton
        if autonMode == 1:
            auton = DriveForwardAuton(logger)
            auton.start()
            self.loop()
        elif autonMode == 0:
            auton = SmartAuton(logger)
            auton.start()
        else: logger.info("Auton(): Autonomous Mode Not Enabled")
        
        
    def loop(self):
        global autonEnabled
        if auton.isFinished():
            self.enableAuton(False)

    def isEnabled(self):
        global autonEnabled
        return autonEnabled
            
    


