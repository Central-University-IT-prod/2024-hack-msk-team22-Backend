import os
from dotenv import load_dotenv
from utils.database import MongoDB



load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
MONGODB_TOKEN = os.getenv("MONGODB_TOKEN")
ALGORITHM = 'HS256'

db = MongoDB(MONGODB_TOKEN)