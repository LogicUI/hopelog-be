from dotenv import load_dotenv
from supabase import create_client, Client
import logging
import os


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Supabase URL or Key is missing")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
