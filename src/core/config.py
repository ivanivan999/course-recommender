# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Course Recommender")
    API_VERSION = os.getenv("API_VERSION", "v1")
    DEBUG = os.getenv("DEBUG", "false").lower() in ["true", "1", "t"]
    DATABASE_URL = os.getenv("DATABASE_URL")
    # Add other configuration variables as needed

config = Config()