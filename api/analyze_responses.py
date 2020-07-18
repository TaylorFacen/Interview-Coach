from dateparser import parse
from flask import request
import json
import matplotlib.pyplot as plt
import os
import re
from wordcloud import WordCloud

from .helper import app, Twilio

@app.route('/api/analyze_responses', methods = ['POST'])
def analyze_responses():  
    """ Analyzes responses and sends results """
    twilio = Twilio()

    req = request.form.to_dict()
    memory = json.loads(req['Memory'])
    responses = memory['responses']
    phone_number = memory['twilio']['voice']['To']
    category = memory['category']

    responses = list(map(lambda response: {
        'question': response['question'],
        'response': response['response'],
        'start': response['start'],
        'end': response['end']
    }, responses))

    document = twilio.get_document(phone_number)
    data = document.data
    data['responses'] = responses
    twilio.update_document(data, phone_number)

    text_data = analyze_interview_response(responses, phone_number, category)
    
    # Send the results back to the user
    twilio.send_sms(text_data['message_1'], phone_number)
    twilio.send_mms(text_data['absolute_file_location'], phone_number)

    actions = {
        "actions": [
            {
                "say": "That was awesome! Check your phone to see my notes. "
            }
        ]
    }

    return actions

### Helper Functions ###
def parse_duration(response):
    """ Returns the length of time used to respond to a question """

    start = parse(response['start'])
    end = parse(response['end'])

    # On average, bot talks at 150 words per minute. 
    average_wpm = 150
    question_word_count = get_word_count(response['question']['question'])
    question_duration_s = (question_word_count / average_wpm) * 60

    total_duration_s = (end - start).seconds
    response_duration_s = total_duration_s - question_duration_s

    return response_duration_s

def get_word_count(text):
    regex = re.compile(r'\w+')
    word_count = len(regex.findall(text))
    return word_count

def calculate_wpm(word_count, seconds):
    return word_count / (seconds / 60)

def get_total_wpm(responses):
    total_wpm = calculate_wpm(
        sum(response['response_word_count'] for response in responses),
        sum(response['response_duration'] for response in responses)
    )

    return total_wpm

def analyze_response_speed(responses):
    message = ""
    
    total_wpm = get_total_wpm(responses)
    message += "Overall, you talked about {0:.0f} words per minute (wpm). ".format(total_wpm)
    
    if total_wpm > 150:
        message += "Try slowing down so that the interviewer is able to understand everything that you're saying. "
    elif total_wpm < 120:
        message += "You have some room to increase your talking speed. "
    else:
        message += "That's a good pace. "
        
    message += "Ideally, it's good to speak within 120 and 150 wpm. "
    
    
    if len(responses) > 1:
        sorted_responses = sorted(responses, key = lambda r: r['response_duration'])
        shortest_response = sorted_responses[0]
        longest_response = sorted_responses[-1]
        
        if longest_response['response_duration'] > 90:
            message += "Your response to '{}' was pretty lengthy. Keeping your responses under 90 seconds ensures that the interview is more of a conversation. ".format(longest_response['question']['question'])
        
        if shortest_response['response_duration'] < 30:
            message += "Your response to '{}' was quite short. The interviewer really wants to get to know you, so feel free to expand on your point a bit more. ".format(shortest_response['question']['question'])
        
        if longest_response['response_duration'] <= 90 and shortest_response['response_duration'] >= 30:
            message += "You did a good job at keeping your answers concise while leaving room for important details. "
    else:
        response = responses[0]
        
        if response['response_duration'] > 90:
            message += "Your response was pretty lengthy. Keeping your responses under 90 seconds ensures that the interview is more of a conversation. "
        elif response['response_duration'] < 30:
            message += "Your response was quite short. The interviewer really wants to get to know you, so feel free to expand on your point a bit more. "
        else:
            message += "You did a good job at keeping your answer concise while leaving room for important details. "
        
    
    return message

def analyze_filler_phrases(responses):
    message = "When speaking, it's best to not use filler words and phrases (basically, kind of, like, etc.). "
    
    filler_phrases = [
        'just',
        'only',
        'really',
        'slightly',
        'almost',
        'seemed',
        'absolutely',
        'basically',
        'actually',
        'sort of',
        'kind of',
        'a little',
        'very',
        'like'
    ]

    filler_phrase_frequencies = {}

    for fp in filler_phrases:
        regex = re.compile(fp)

        for response in list(map(lambda r: r['response'], responses)):
            filler_phrase_frequencies[fp] = filler_phrase_frequencies.get(fp, 0) + len(regex.findall(response, re.IGNORECASE))
            
    filler_phrase_frequencies = {k:v for k, v in filler_phrase_frequencies.items() if v > 0 }
    
    if len(filler_phrase_frequencies) > 0:
        total_word_count = sum([response['response_word_count'] for response in responses])
        total_filler_phrase_count = sum(filler_phrase_frequencies.values())

        filler_phrase_percent = total_filler_phrase_count / total_word_count
        
        if filler_phrase_percent > .10:
            message += "{0:.0%} of your responses were filler words. Try to bring that down so that your answers sound more confident. ".format(filler_phrase_percent)
        else:
            message += "You didn't use a lot of filler phrases in your responses. It's natural for a few of these to come up in conversation. Good job at keeping it under control.  "    
            
    else:
        message += "Good job on not using any filler words in your answers! "
        
    return message

def generate_word_cloud(responses, phone_number):
    file_name = "word_cloud_{}.png".format(phone_number.replace('+', ''))
    folder = 'tmp/'
    all_responses = ' '.join(list(map(lambda r: r['response'], responses)))
    wordcloud = WordCloud(background_color="white").generate(all_responses)
    wordcloud.to_file(folder + file_name)
    
    return file_name

def analyze_interview_response(responses, phone_number, category):
    text_data = {}

    for response in responses:
        response['response_duration'] = parse_duration(response)
        response['response_word_count'] = get_word_count(response['response'])

    message = "Here's how you did on your {} interview practice.\n".format(category.title())
    message += analyze_response_speed(responses)

    message += '\n\n'

    message += analyze_filler_phrases(responses)
    file_name = generate_word_cloud(responses, phone_number)
    # Get full file path - Using this because I have no idea where Vercel places temporary files
    for root, dirs, files in os.walk(os.getcwd()):
        if file_name in files:
            absolute_file_location = os.path.join(root, file_name)
            break
    
    text_data['message_1'] = message
    text_data['file_name'] = file_name
    text_data['absolute_file_location'] = absolute_file_location
    text_data['phone_number'] = phone_number

    return text_data

