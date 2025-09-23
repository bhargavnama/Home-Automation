from typing import Optional, Dict, List
from src.dao.home_controller_dao import HomeController as HomeControllerDAO
from src.dao.device_dao import Device as DeviceDAO


class HomeControllerService:
    
    def __init__(self):
        self._dao = HomeControllerDAO()
        self._devices = DeviceDAO()
    
    def create_controller(self, name: str, location: str, user_id: int) -> Optional[Dict]:
        return self._dao.create_controller(name, location, user_id)
    
    def add_device(self, type_name: str, name: str, status: bool, location: str, user_id: int) -> Optional[Dict]:
        return self._devices.create_device(type_name, name, status, location, user_id)
    
    def list_user_devices(self, user_id: int) -> List[Dict]:
        return self._devices.list_devices_by_user(user_id)

