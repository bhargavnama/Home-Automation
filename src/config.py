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
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Supabase url and Supabase key must be assigned in the .env")
    else:
        return create_client(SUPABASE_URL, SUPABASE_KEY)