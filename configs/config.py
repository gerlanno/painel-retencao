import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    ATRIX_HOST = os.getenv("ATRIX_HOST")
    ATRIX_DB = os.getenv("ATRIX_DB")
    ATRIX_USER = os.getenv("ATRIX_USER")
    ATRIX_PASSWORD = os.getenv("ATRIX_PASSWORD")

    SUPABASE_HOST = os.getenv("SUPABASE_HOST")
    SUPABASE_DB = os.getenv("SUPABASE_DB")
    SUPABASE_USER = os.getenv("SUPABASE_USER")
    SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")
    SUPABASE_PORT = os.getenv("SUPABASE_PORT")