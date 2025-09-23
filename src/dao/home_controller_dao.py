from src.config import get_supabase
from typing import Optional, Dict

class HomeController:
    
    def __init__(self):
        self._sb = get_supabase()
        
    def create_controller(self, name: str, location: str, user_id: int) -> Optional[Dict]:
        """
        
            Creates a new controller and returns its details
        """
        
        payload = {
            "name": name,
            "location": location,
            "user_id": user_id
        }
        
        resp = self._sb.table("home_controller").insert(payload).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    def update_controller(self, controller_id: int, fields: Dict) -> Optional[Dict]:
        """
        
            Updates the details of a controller and returns the updated info 
        """
        
        resp = self._sb.table("home_controller").update(fields).eq("controller_id", controller_id).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    def get_controller_info_by_id(self, controller_id: int) -> Optional[Dict]:
        """
        
            Returns the details of a controller
        """
        
        resp = self._sb.table("home_controller").select("*").eq("controller_id", controller_id).limit(1).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    
    def delete_controller(self, controller_id: int) -> Optional[Dict]:
        """
        
            Removes a controller from the db
        """
        
        before = self._sb.table("home_controller").select("*").eq("controller_id", controller_id).limit(1).execute()
        self._sb.table("home_controller").delete().eq("controller_id", controller_id).execute()
        return before.data[0] if (before.data and len(before.data) > 0) else None