from typing import Optional
from src.devices.smart_device import SmartDevice


class LightDevice(SmartDevice):
    
    def set_brightness(self, level: int) -> Optional[dict]:
        if level < 0:
            level = 0
        if level > 100:
            level = 100
        updated = self._dao.set_device_setting(self.device_id, "brightness", str(level))
        if updated:
            self._dao.log_device_action(self.device_id, f"set_brightness:{level}")
        return updated

