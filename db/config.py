import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

FOLDER = "cards/"
