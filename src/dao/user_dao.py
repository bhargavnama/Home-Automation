from src.config import get_supabase
from typing import Optional, Dict

class User:
    
    def __init__(self):
        self._sb = get_supabase()
        
    def create_user(self, name: str, email: str, phone: str, city:str) -> Optional[Dict]:
        """
        
            creates a new user and returns the created users data
        """
        payload = { "name": name, "email": email, "phone": phone, "city": city }
        resp = self._sb.table("users").insert(payload).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    def update_user(self, user_id: int, fields: dict) -> Optional[Dict]:
        """
            updates the existing user data
        """
        
        resp = self._sb.table("users").update(fields).eq("user_id", user_id).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    def delete_user(self, user_id: int) -> Optional[Dict]:
        """
        
            Removes an user from the database and returns the information of the user
        """
        
        before = self._sb.table("users").select("*").eq("user_id", user_id).limit(1).execute()
        self._sb.table("users").delete().eq("user_id", user_id).execute()
        return before.data[0] if (before.data and len(before.data) > 0) else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        
            Search for a user by their id and returns if exists else returns None
        """
        
        resp = self._sb.table("users").select("*").eq("user_id", user_id).limit(1).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        
            Search for a user by their email and returns if exists else returns None
        """
        
        resp = self._sb.table("users").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if (resp.data and len(resp.data) > 0) else None