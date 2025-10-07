from src.config import get_supabase
from typing import Optional, Dict, List

class Device:
    
    def __init__(self):
        self._sb = get_supabase()
        
    def _get_or_create_type(self, type_name: str) -> Optional[int]:
        """
            Returns type_id for the given type_name, creating it if missing.
        """
        type_select = self._sb.table("device_types").select("type_id").eq("type_name", type_name).limit(1).execute()
        if type_select.data and len(type_select.data) > 0:
            return type_select.data[0]["type_id"]
        insert_resp = self._sb.table("device_types").insert({"type_name": type_name}).execute()
        if insert_resp.data and len(insert_resp.data) > 0:
            return insert_resp.data[0]["type_id"]
        return None
        
    def create_device(self, type_name: str, name: str, status: bool, location: str, user_id: int) -> Optional[Dict]:
        """
            Creates a new device and returns the created row.
        """
        type_id = self._get_or_create_type(type_name)
        if type_id is None:
            return None
        payload = {
            "name": name,
            "status": status,
            "location": location,
            "type_id": type_id,
            "user_id": user_id,
        }
        resp = self._sb.table("devices").insert(payload).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    def update_device(self, device_id: int, fields: Dict) -> Optional[Dict]:
        """
            Updates an existing device by device_id and returns the updated row.
        """
        if "type_name" in fields:
            resolved_type_id = self._get_or_create_type(fields.pop("type_name"))
            if resolved_type_id is None:
                return None
            fields["type_id"] = resolved_type_id
        resp = self._sb.table("devices").update(fields).eq("device_id", device_id).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    def delete_device(self, device_id: int) -> Optional[Dict]:
        """
            Removes a device and returns the deleted device data.
        """
        before = self._sb.table("devices").select("*").eq("device_id", device_id).limit(1).execute()
        self._sb.table("devices").delete().eq("device_id", device_id).execute()
        return before.data[0] if (before.data and len(before.data) > 0) else None
    
    def get_device_by_id(self, device_id: int) -> Optional[Dict]:
        """
            Fetch a device by id.
        """
        resp = self._sb.table("devices").select("*").eq("device_id", device_id).limit(1).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    def list_devices_by_user(self, user_id: int) -> List[Dict]:
        """
            List all devices for a given user_id.
        """
        # Fetch devices first
        resp = self._sb.table("devices").select("*").eq("user_id", user_id).execute()
        devices = resp.data or []
        if not devices:
            return []
        # Build a unique list of type_ids present
        type_ids = sorted({d.get("type_id") for d in devices if d.get("type_id") is not None})
        if not type_ids:
            return devices
        # Fetch type names in one query
        type_rows = self._sb.table("device_types").select("type_id,type_name").in_("type_id", type_ids).execute()
        id_to_name = {row["type_id"]: row.get("type_name") for row in (type_rows.data or [])}
        # Annotate devices with type_name for UI convenience
        for d in devices:
            tid = d.get("type_id")
            if tid in id_to_name:
                d["type_name"] = id_to_name.get(tid)
        return devices
    
    def get_devices_by_type_name(self, type_name: str) -> List[Dict]:
        """
            List all devices for a given device type name.
        """
        type_id = self._get_or_create_type(type_name)
        if type_id is None:
            return []
        resp = self._sb.table("devices").select("*").eq("type_id", type_id).execute()
        devices = resp.data or []
        # Attach type_name for convenience
        for d in devices:
            d["type_name"] = type_name
        return devices
    
    def set_device_setting(self, device_id: int, attribute: str, value: str) -> Optional[Dict]:
        """
            Upserts a device setting (attribute, value) for the device.
            Requires a unique constraint on (device_id, attribute) in the backend for on_conflict.
        """
        payload = { "device_id": device_id, "attribute": attribute, "value": value }
        resp = self._sb.table("device_settings").upsert(payload, on_conflict="device_id,attribute").execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    def get_device_settings(self, device_id: int) -> List[Dict]:
        """
            Returns all settings for a device.
        """
        resp = self._sb.table("device_settings").select("*").eq("device_id", device_id).execute()
        return resp.data or []
    
    def log_device_action(self, device_id: int, action: str) -> Optional[Dict]:
        """
            Writes a log entry for a device action.
            Assumes the backend has default timestamp for the column.
        """
        resp = self._sb.table("device_logs").insert({"device_id": device_id, "action": action}).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None