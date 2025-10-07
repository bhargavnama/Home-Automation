from dotenv import load_dotenv
from supabase import create_client, Client
import os

# Load environment variables from a local .env file if present
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def get_supabase() -> Client:
    """
        Returns a supabase client. Raises RuntimeError if config missing.
    """
    url = SUPABASE_URL
    key = SUPABASE_KEY
    if not url or not key:
        try:
            import streamlit as st
            # Prefer flat secrets keys; fallback raises KeyError if missing
            url = url or st.secrets.get('SUPABASE_URL')
            key = key or st.secrets.get('SUPABASE_KEY')
        except Exception:
            pass
    if not url or not key:
        raise RuntimeError("Supabase url and Supabase key must be set via environment variables or Streamlit secrets.")
    return create_client(url, key)