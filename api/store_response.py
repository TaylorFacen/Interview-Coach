from flask import request
import json

from .app import app
from .config import VERCEL_URL

@app.route('/api/store_response', methods = ['POST'])
def store_response():
    """ Store's the user's response in memory and routes to the next action """
    req = request.form.to_dict()
    memory = json.loads(req['Memory'])
    responses = memory['responses']
    remaining_questions = memory['remaining_questions']
    current_question = memory['current_question']

    collected_data = memory['twilio']['collected_data']

    start = collected_data['date_started']
    end = collected_data['date_completed']
    response = collected_data['answers']['response']['answer']

    responses.append({
        'question': current_question,
        'response': response,
        'start': start,
        'end': end
    })

    if len(remaining_questions) > 0:
        redirect = "{}/api/ask_question".format(VERCEL_URL)
    else:
        redirect = "{}/api/analyze_responses".format(VERCEL_URL)

    actions = {
        "actions": [
            {
                "remember": {
                    'responses': responses
                }
            }, {
                'redirect': {
                    'uri': redirect
                }
            }
        ]
    }

    return actions