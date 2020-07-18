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

# AWS Credentials
IC_S3_BUCKET = os.environ['IC_S3_BUCKET']
IC_AWS_DEFAULT_REGION = os.environ['IC_AWS_DEFAULT_REGION']
IC_AWS_SECRET_ACCESS_KEY = os.environ['IC_AWS_SECRET_ACCESS_KEY']
IC_AWS_ACCESS_KEY_ID = os.environ['IC_AWS_ACCESS_KEY_ID']