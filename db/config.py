import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

PROXY = {
    "http": os.getenv("PROXY_HTTP"),
    "https": os.getenv("PROXY_HTTPS")
}

FOLDER = "cards/"
