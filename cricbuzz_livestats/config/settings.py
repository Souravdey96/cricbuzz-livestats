import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
DB_PATH = os.getenv('DB_PATH')
DB_URL = f"sqlite:///{DB_PATH}"