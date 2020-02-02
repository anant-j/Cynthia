from flask import Flask
from flask import request
import json
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

anger = 0
fear = 0
joy = 0
sadness = 0
analytical = 0
confident = 0
tentative = 0
numOfSentences = 0


app = Flask(__name__)

with open('twilio_keys.json') as f:
    tw_keys = json.load(f)
    account_sid = tw_keys['MY_ACCOUNT_SID']
    auth_token = tw_keys['MY_AUTH_TOKEN']

client = Client(account_sid, auth_token)
PAPERQUOTES_API_ENDPOINT = 'http://api.paperquotes.com/apiv1/quotes?tags=love&limit=5'
TOKEN = '5c62454a0cf6fb27d2cdc79edecb890eb16e7d0e'


@app.route('/q/', methods=['GET'])
def sendQuote():
    response = requests.get(PAPERQUOTES_API_ENDPOINT, headers={'Authorization': 'TOKEN {}'.format(TOKEN)})

    if response.ok:

        quotes = json.loads(response.text).get('results')

        for quote in quotes:
            print(quote.get('quote'))
            print(quote.get('author'))
            print(quote.get('tags'))
    return


@app.route('/', methods=['GET'])
def send():
    global anger
    global fear
    global joy
    global sadness
    global analytical
    global confident
    global tentative
    arr = [anger, fear, joy, sadness, analytical, confident, tentative]
    arr.sort()
    if anger == arr.index(0):
        first = anger
    elif anger == arr.index(1):
        second = anger
    elif fear == arr.index(0):
        first = fear
    elif fear == arr.index(1):
        second = fear
    elif joy == arr.index(0):
        first = joy
    elif joy == arr.index(1):
        second = joy
    elif sadness == arr.index(0):
        first = sadness
    elif sadness == arr.index(1):
        second = sadness
    elif confident == arr.index(0):
        first = confident
    elif confident == arr.index(1):
        second = confident
    elif analytical == arr.index(0):
        first = analytical
    else:
        second = analytical
    return json.dumps({"response": str(first + ',' + second)})


@app.route('/', methods=['POST'])
def receive():
    headers = {
        'Content-Type': 'application/json',
    }
    d = {}
    inp_data = str(request.form['request'])
    global numOfSentences
    numOfSentences += 1
    x = {
        "text": inp_data
    }
    data = json.dumps(x)
    response = requests.post(
        'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/9decad53-7281-4d48-8c86-f105d1f42122/v3/tone?version=2017-09-21',
        headers=headers, data=data, auth=('apikey', 'key'))
    for responses in response.json()['document_tone']['tones']:
        d[str(responses['tone_id'])] = responses['score']
        if responses['tone_id'] is 'anger':
            global anger
            if anger is None:
                anger = 0
            anger += responses['score']
        elif responses['tone_id'] is 'fear':
            global fear
            if fear is None:
                fear = 0
            fear += responses['score']
        elif responses['tone_id'] is 'joy':
            global joy
            if joy is None:
                joy = 0
            joy += responses['score']
        elif responses['tone_id'] is 'sadness':
            global sadness
            if sadness is None:
                sadness = 0
            sadness += responses['score']
        elif responses['tone_id'] is 'confident':
            global confident
            if confident is None:
                confident = 0
            confident += responses['score']
        else:
            global analytical
            if analytical is None:
                analytical = 0
            analytical += responses['score']
    return str(d)


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
    d = {}
    x = {
        "text": content
    }
    data = json.dumps(x)
    response = requests.post(
        'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/9decad53-7281-4d48-8c86-f105d1f42122/v3/tone?version=2017-09-21',
        headers=headers, data=data, auth=('apikey', 'key'))
    for responses in response.json()['document_tone']['tones']:
        d[str(responses['tone_id'])] = responses['score']
        if responses['tone_id'] is 'anger':
            global anger
            if anger is None:
                anger = 0
            anger += responses['score']
        elif responses['tone_id'] is 'fear':
            global fear
            if fear is None:
                fear = 0
            fear += responses['score']
        elif responses['tone_id'] is 'joy':
            global joy
            if joy is None:
                joy = 0
            joy += responses['score']
        elif responses['tone_id'] is 'sadness':
            global sadness
            if sadness is None:
                sadness = 0
            sadness += responses['score']
        elif responses['tone_id'] is 'confident':
            global confident
            if confident is None:
                confident = 0
            confident += responses['score']
        else:
            global analytical
            if analytical is None:
                analytical = 0
            analytical += responses['score']
    return str(d)


if __name__ == '__main__':
    app.run()
