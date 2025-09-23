from typing import Optional
from src.devices.smart_device import SmartDevice


class CameraDevice(SmartDevice):
    
    def start_recording(self) -> Optional[dict]:
        updated = self._dao.set_device_setting(self.device_id, "recording", "on")
        if updated:
            self._dao.log_device_action(self.device_id, "start_recording")
        return updated
    
    def stop_recording(self) -> Optional[dict]:
        updated = self._dao.set_device_setting(self.device_id, "recording", "off")
        if updated:
            self._dao.log_device_action(self.device_id, "stop_recording")
        return updated

