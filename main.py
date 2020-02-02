from flask import Flask
from flask import request
import json
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

app = Flask(__name__)

with open('twilio_keys.json') as f:
    tw_keys = json.load(f)
    account_sid = tw_keys['MY_ACCOUNT_SID']
    auth_token = tw_keys['MY_AUTH_TOKEN']

client = Client(account_sid, auth_token)

@app.route('/', methods=['GET'])
def send():
    return (json.dumps({"response": str("Thank you for using the service.")}))

@app.route('/', methods=['POST'])
def receive():
    headers = {
        'Content-Type': 'application/json',
    }
    d={}
    inp_data = str(request.form['request'])
    x = {
  "text": inp_data
    }
    data = json.dumps(x)
    response = requests.post(
        'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/9decad53-7281-4d48-8c86-f105d1f42122/v3/tone?version=2017-09-21',
        headers=headers, data=data, auth=('apikey', 'key'))
    for responses in response.json()['document_tone']['tones']:  
        d[str(responses['tone_id'])]=responses['score']
    return(str(d))

@app.route('/sms', methods=['POST'])
def sms():
    message_content = request.values.get('Body', None)
    contact = request.values.get('From', None)
    try:
        res = send_sms(message_content, contact)
        # resp = MessagingResponse()
        # resp.message(res)
        return ("SMS Message Sent", 200)
    except Exception as e:
        return ("An Error Occured while sending SMS", e)


def send_sms(message_content, contact):
    client.messages.create(
    to=contact,
    from_=tw_keys['MY_TWILIO_NUMBER'],
    body=str(receiveContent(str(message_content)))
    )

def receiveContent(content):
    headers = {
        'Content-Type': 'application/json',
    }
    d={}
    x = {
  "text": content
    }
    data = json.dumps(x)
    response = requests.post(
        'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/9decad53-7281-4d48-8c86-f105d1f42122/v3/tone?version=2017-09-21',
        headers=headers, data=data, auth=('apikey', 'key'))
    for responses in response.json()['document_tone']['tones']:  
        d[str(responses['tone_id'])]=responses['score']
    return(str(d))

if __name__ == '__main__':
    app.run()
