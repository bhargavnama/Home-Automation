from typing import Optional
from src.devices.smart_device import SmartDevice


class ThermostatDevice(SmartDevice):
    
    def set_temperature(self, celsius: float) -> Optional[dict]:
        updated = self._dao.set_device_setting(self.device_id, "temperature_c", str(celsius))
        if updated:
            self._dao.log_device_action(self.device_id, f"set_temperature:{celsius}")
        return updated

