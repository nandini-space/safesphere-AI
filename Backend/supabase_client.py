import os
from dotenv import load_dotenv
from supabase import create_client


# Load environment variables from backend/.env
load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Check credentials
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing from .env")


# Create Supabase client
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)