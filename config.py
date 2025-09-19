# In sagar-main-api/config.py

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Create a single Supabase client instance
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set. Please check your .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)