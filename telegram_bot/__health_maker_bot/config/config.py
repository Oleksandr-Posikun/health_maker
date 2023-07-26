import os
import logging
# from openrouteservice import client
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
# CLIENT = client.Client(key=str(os.getenv("MAP_API_KEY")))
ADMINS = os.getenv("ADMIN").split(',')
