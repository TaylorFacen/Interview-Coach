from .helper import app, Twilio

twilio = Twilio()

@app.route('/api/connect_call', methods = ['POST'])
def connect_call():
    """ Connects the call to autopilot """
    response = twilio.connect_call()
    return response