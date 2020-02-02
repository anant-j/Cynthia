from flask import Flask
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def request():
    return 'this is a post request'


@app.route('/', methods=['GET'])
def receive():
    # return("Hello")
    headers = {
        'Content-Type': 'application/json',
    }
    d={}
    data = open('tone.json', 'rb').read()
    response = requests.post(
        'url',
        headers=headers, data=data, auth=('apikey', 'key'))
    for responses in response.json()['document_tone']['tones']:  
        d[str(responses['tone_id'])]=responses['score']
    return(str(d))


if __name__ == '__main__':
    app.run()
