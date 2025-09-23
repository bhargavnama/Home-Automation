from typing import Optional, List, Dict
from src.dao.device_dao import Device as DeviceDAO
from src.devices.light_device import LightDevice
from src.devices.thermostat_device import ThermostatDevice
from src.devices.camera_device import CameraDevice


class DeviceService:
    
    def __init__(self):
        self._dao: DeviceDAO = DeviceDAO()
    
    def create(self, type_name: str, name: str, status: bool, location: str, user_id: int) -> Optional[Dict]:
        return self._dao.create_device(type_name, name, status, location, user_id)
    
    def by_user(self, user_id: int) -> List[Dict]:
        return self._dao.list_devices_by_user(user_id)
    
    def get(self, device_id: int) -> Optional[Dict]:
        return self._dao.get_device_by_id(device_id)
    
    def control_on(self, device_id: int) -> Optional[Dict]:
        info = self._dao.get_device_by_id(device_id)
        if not info:
            return None
        tname = info.get("type_name")
        # If type_name not present, try to infer via join in app layer (fallback to generic)
        if tname == "Light":
            return LightDevice(device_id).turn_on()
        elif tname == "Thermostat":
            return ThermostatDevice(device_id).turn_on()
        elif tname == "Camera":
            return CameraDevice(device_id).turn_on()
        else:
            from src.devices.smart_device import SmartDevice
            return SmartDevice(device_id).turn_on()
    
    def control_off(self, device_id: int) -> Optional[Dict]:
        from src.devices.smart_device import SmartDevice
        return SmartDevice(device_id).turn_off()

