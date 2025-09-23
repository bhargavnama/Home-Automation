from typing import Optional
from src.dao.device_dao import Device as DeviceDAO


class SmartDevice:
    
    def __init__(self, device_id: int):
        self._dao = DeviceDAO()
        self.device_id = device_id
    
    def turn_on(self) -> Optional[dict]:
        updated = self._dao.update_device(self.device_id, {"status": True})
        if updated:
            self._dao.log_device_action(self.device_id, "turn_on")
        return updated
    
    def turn_off(self) -> Optional[dict]:
        updated = self._dao.update_device(self.device_id, {"status": False})
        if updated:
            self._dao.log_device_action(self.device_id, "turn_off")
        return updated
    
    def get_info(self) -> Optional[dict]:
        return self._dao.get_device_by_id(self.device_id)

