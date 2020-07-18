from flask import request
import json

from .helper import app, Twilio

@app.route('/api/process_interview_request', methods = ['POST'])
def process_interview_request():
    """ Process an incoming interview request from the Autopilot conversation """
    twilio = Twilio()
    
    req = request.form.to_dict()
    memory = json.loads(req['Memory'])
    phone_number = memory['twilio']['sms']['From']

    answers = memory['twilio']['collected_data']['category_selection']['answers']
    limit = answers['limit']['answer']
    category = answers['category']['answer']

    data = json.dumps({
        'limit': limit,
        'category': category    
    })

    # Store session information via Twilio Sync
    twilio.store_document(data, phone_number)

    # Call user
    twilio.call_user(phone_number)

    actions = {
        "actions": [
            {
                "say": "Calling now."
            }
        ]
    }

    return actions
