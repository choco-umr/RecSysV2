import os
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")

CONNECTION_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

MEMORY_COST = os.getenv("MEMORY_COST")
TIME_COST = os.getenv("TIME_COST")
PARALLELISM = os.getenv("PARALLELISM")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRY_TIME = os.getenv("EXPIRY_TIME")