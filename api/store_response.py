from flask import request
import json

from .helper import app
from .helper.config import VERCEL_URL

@app.route('/api/store_response', methods = ['POST'])
def store_response():
    """ Store's the user's response in memory and routes to the next action """
    req = request.form.to_dict()
    memory = json.loads(req['Memory'])
    responses = memory['responses']
    remaining_questions = memory['remaining_questions']
    current_question = memory['current_question']

    interview_question = memory['twilio']['collected_data']['interview_question']
    start = interview_question['date_started']
    end = interview_question['date_completed']
    response = interview_question['answers']['response']['answer']

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