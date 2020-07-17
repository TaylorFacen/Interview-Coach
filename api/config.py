import os

from dotenv import load_dotenv

MONGO_URL = os.environ['MONGO_URL']
VERCEL_URL = os.environ['VERCEL_URL']

# Twilio Credentials
ACCOUNT_SID = os.environ['ACCOUNT_SID']
ASSISTANT_SID = os.environ['ASSISTANT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
SYNC_SERVICE_SID = os.environ['SYNC_SERVICE_SID']
TWILIO_NUMBER = os.environ['TWILIO_NUMBER']