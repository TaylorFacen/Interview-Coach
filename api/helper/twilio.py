from flask import make_response
from twilio.rest import Client
from twilio.twiml.voice_response import Connect, VoiceResponse

from .aws import upload_file
from .config import VERCEL_URL, ACCOUNT_SID, ASSISTANT_SID, AUTH_TOKEN, SYNC_SERVICE_SID, TWILIO_NUMBER

class Twilio:
    def __init__(self):
        self.ASSISTANT_SID = ASSISTANT_SID
        self.SYNC_SERVICE_SID = SYNC_SERVICE_SID
        self.TWILIO_NUMBER = TWILIO_NUMBER
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    def call_user(self, phone_number):
        call = self.client.calls.create(
            url = "{}/api/connect_call".format(VERCEL_URL),
            to = phone_number,
            from_ = self.TWILIO_NUMBER
        )
    
    def connect_call(self):
        """ Connect the call to autopilot """
        response = VoiceResponse()

        connect = Connect()
        connect.autopilot(self.ASSISTANT_SID, TargetTask = "conduct_interview")
        response.append(connect)
        response = make_response(str(response))
        response.headers['Content-type'] = 'text/html; charset=utf-8'

        return response
    
    def get_document(self, phone_number):
        document = self.client.sync.services(self.SYNC_SERVICE_SID) \
            .documents(phone_number) \
                .fetch()
                
        return document
    
    def send_mms(self, file_path, phone_number):
        file_url = upload_file(file_path)
        self.client.messages.create(
            body = "Here's a word cloud of your top used words.", 
            from_ = self.TWILIO_NUMBER,
            media_url = [file_url],
            to = phone_number
        )

    def send_sms(self, message, phone_number):
        self.client.messages.create(
            body = message,
            from_ = self.TWILIO_NUMBER,
            to = phone_number
        )
        return None

    def store_document(self, data, phone_number):
        """ Store information in Sync document """
        try:
            document = self.client.sync.services(self.SYNC_SERVICE_SID) \
                .documents \
                    .create(data = data, unique_name = phone_number)
        except:
            # There's already a document for this phone number
            self.client.sync.services(self.SYNC_SERVICE_SID) \
                .documents(phone_number) \
                    .delete()
            
            document = self.client.sync.services(self.SYNC_SERVICE_SID) \
                .documents \
                    .create(data = data, unique_name = phone_number)

    def update_document(self, data, phone_number):
        """ Updates an existing document """
        try:
            self.client.sync.services(self.SYNC_SERVICE_SID) \
                .documents(phone_number) \
                    .delete()
        except:
            None
        
        self.client.sync.services(self.SYNC_SERVICE_SID) \
            .documents \
                .create(data = data, unique_name = phone_number)