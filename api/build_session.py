import json
from flask import request

from .app import app
from .config import VERCEL_URL
from .db import 
from .twilio import Twilio

twilio = Twilio()

@app.route('/api/build_session', methods = ['POST'])
def build_session():
    """ Builds the questions lists for the interview """
    req = request.form.to_dict()
    memory = json.loads(req['Memory'])
    phone_number = memory['twilio']['voice']['To']

    # Get session details from sync
    document = twilio.get_document(phone_number)
    data = document.data

    limit = data['limit']
    category = data['category']

    questions = db.get_questions(category = category, limit = limit)
    # Reformat ObjectIds
    questions = list(map(lambda question: {
        "id": str(question['_id']),
        "question": question['question'],
        "categoryId": str(question['categoryId']), 
        "category": question['category']
    }, questions))

    # Store questions in memory
    actions = {
        "actions": [
            {
                "remember": {
                    "remaining_questions": questions,
                    "responses": [],
                    "category": category
                }
            }, {
                "redirect": {
                    "uri": "{}/api/ask_question".format(VERCEL_URL)
                }
            }
        ]
    }

    return response