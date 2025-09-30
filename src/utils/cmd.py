import logging
import platform
import subprocess
import json

logger = logging.getLogger(__name__)

class Command:

    def __init__(self,prompt):
        self.prompt = prompt
        self.result = None

    def execute(self):
        self._process()
        return self.result

    def _process(self):
        system = platform.system()
        
        if system == "Windows":
            logger.debug("Process Window's command")
            self.powershell()
        else:
            logger.error(f"Undefined operating system")
        
    def powershell(self)->json:
        logger.debug(f"Command: '{self.prompt}'")
        result = subprocess.run(
            ["powershell", "-Command", self.prompt],
            capture_output=True,  # capture stdout and stderr
            text=True             # return output as string
        )
        if result.returncode != 0:
            logger.warning(f"Powershell Error {self.prompt}")
            return ""
        self.result = result.stdout
        return self.result