import wmi
import json
import logging
import platform
from src.utils.cmd import Command

logger = logging.getLogger(__name__)

class Pc:
    def __init__(self):
        self._os             = None
        self._cpu            = None
        self._ram            = None
        self._storage        = None
        self._gpu            = None
        self._motherboard    = None
        self._wmi_connection = None
        self._connection()
    
    def _connection(self):
        try:
            if platform.system().lower() == "windows":
                self._wmi_connection = wmi.WMI()
        except Exception as e:
            logger.warning(e)

    def _get_prop(self,win_obj):
        return {prop: getattr(win_obj, prop) for prop in win_obj.properties.keys()}

    def _load_wmi_disks(self)->json:
        cmd = Command("Get-PhysicalDisk | Select-Object SerialNumber, MediaType | ConvertTo-Json")
        try:
            output = cmd.execute()
            result = json.loads(output)
            logger.debug(f"PowerShell return: {result}")
            return result
            
        except Exception as e:
            logger.error("Failed to load WMI disk:",e)

    @property
    def os(self):
        logger.debug("Accessing Operating System")
        if self._os == None:
            self._os = self._wmi_connection.Win32_OperatingSystem()[0].Caption
        return self._os

    @property
    def ram(self):
        logger.debug("Accessing RAM")
        if self._ram == None:
            self._ram = [self._get_prop(ram) for ram in self._wmi_connection.Win32_PhysicalMemory()]
        return self._ram

    @property
    def cpu(self):
        logger.debug("Accessing CPU")
        if self._cpu == None:
            self._cpu = [self._get_prop(cpu) for cpu in self._wmi_connection.Win32_Processor()]
        return self._cpu

    @property
    def storage(self):
        logger.debug("Accessing storage")
        if self._storage == None:
            self._storage = [self._get_prop(storage) for storage in self._wmi_connection.Win32_DiskDrive()]
            logger.debug(f"Storage size:{len(self._storage)}")
            disks = self._load_wmi_disks()
            for disk in disks:
                for index in range(len(self._storage)):
                    sn = disk.get("SerialNumber").strip()
                    wmi_mediaType = disk.get("MediaType","Unspecified")
                    if sn == self._storage[index].get("SerialNumber","").strip() and wmi_mediaType != "Unspecified":
                        logger.debug(f"Serial number match, updating {self._storage[index].get("SerialNumber")} -> {wmi_mediaType}")
                        self._storage[index]["MediaType"] = wmi_mediaType
                        break

        return self._storage
    
    @property
    def motherboard(self):
        logger.debug("Accessing motherboard")
        if self._motherboard == None:
            self._motherboard = [self._get_prop(motherboard) for motherboard in self._wmi_connection.Win32_BaseBoard()]
        return self._motherboard
    
    @property
    def gpu(self):
        logger.debug("Accessing GPU")
        if self._gpu == None:
            self._gpu = [self._get_prop(gpu) for gpu in self._wmi_connection.Win32_VideoController()]
        return self._gpu
    
    @property
    def get_all_props(self):
        return {
            "os":self.os,
            "cpu":self.cpu,
            "storage":self.storage,
            "motherboard":self.motherboard,
            "gpu":self.gpu,
            "ram":self.ram
        }
    
    @property
    def system_info(self):
        return {
            "os":self.os,
            "cpu":[{"Name":cpu.get("Name"),"SerialNumber":cpu.get("SerialNumber"),"ProcessorId":cpu.get("ProcessorId")} for cpu in self.cpu],
            "storage":[{"Model":disk.get("Model"),"SerialNumber":disk.get("SerialNumber"),"MediaType":disk.get("MediaType"),"Size":disk.get("Size")}for disk in self.storage],
            "motherboard":[{"SerialNumber":motherboard.get("SerialNumber")} for motherboard in self.motherboard],
            "gpu":[{"Name":gpu.get("Name")} for gpu in self.gpu],
            "ram":[{"Capacity":ram.get("Capacity")} for cnt,ram in enumerate(self.ram)]
        }
