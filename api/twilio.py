from flask import make_response
from twilio.rest import Client
from twilio.twiml.voice_response import Connect, VoiceResponse

from .config import VERCEL_URL, ACCOUNT_SID, ASSISTANT_SID, AUTH_TOKEN, SYNC_SERVICE_SID, TWILIO_NUMBER

class Twilio:
    def __init__(self):
        self.ASSISTANT_SID = ASSISTANT_SID
        self.SYNC_SERVICE_SID = SYNC_SERVICE_SID
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    def call_user(self, phone_number):
        call = self.client.calls.create(
            url = "{}/api/connect_call".format(VERCEL_URL),
            to = phone_number,
            from_ = TWILIO_NUMBER
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
