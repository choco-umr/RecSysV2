import os

from dotenv import load_dotenv

load_dotenv()

password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")
user = os.getenv("user")
connection_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
memory_cost = os.getenv("memory_cost")
time_cost = os.getenv("time_cost")
parallelism = os.getenv("parallelism")
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")
expiry_time = os.getenv("expiry_time")
max_file_size = os.getenv("max_file_size")