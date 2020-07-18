from flask import request
import json

from .helper import app
from .helper.config import VERCEL_URL

@app.route('/api/ask_question', methods = ['POST'])
def ask_question():
    """ Asks one of the remaining questions """
    req = request.form.to_dict()
    memory = json.loads(req['Memory'])
    remaining_questions = memory['remaining_questions']
    question = remaining_questions.pop()

    actions = {
        "actions": [
            {
                "remember": {
                    "current_question": question,
                    "remaining_questions": remaining_questions
                }
            },
            {
                "collect": {
                    "name": "interview_question",
                    "questions": [
                        {
                            "question": question['question'],
                            "name": "response"
                        }
                    ],
                    "on_complete": {
                        "redirect": "{}/api/store_response".format(VERCEL_URL)
                    }
                }
            }
        ]
    }

    return actions