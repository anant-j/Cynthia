from flask import Flask
from flask import request
import json
import requests

app = Flask(__name__)

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
    print(data)
    response = requests.post(
        'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/9decad53-7281-4d48-8c86-f105d1f42122/v3/tone?version=2017-09-21',
        headers=headers, data=data, auth=('apikey', 'key'))
    for responses in response.json()['document_tone']['tones']:  
        d[str(responses['tone_id'])]=responses['score']
    print(str(d))
    return (json.dumps({"response": str("Please check console for results!")}))


if __name__ == '__main__':
    app.run()
