from drive.DriveControl import DriveControl
class SmartAuton:
    def __init__(self, Logger):
        global logger
        global drive
        logger = Logger
        logger.info("Robot | Code: SmartAuton.py Init")
        drive = DriveControl(logger)

    def start(self):
        logger.info("Auton: Starting SmartAuton...")
        global start
        start = True
        asyncio.run(self.initialize())

    async def initialize(self):
        #OPTIONAL, RUNS ONCE AT START AND IS ASYNC
        logger.info("AUTON INITIALIZE")
        drive.driveDistAuton(10, 20)
