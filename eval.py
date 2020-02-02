import json

import requests
from flask import request

headers = {
        'Content-Type': 'application/json',
}
file = open('text.txt','r', encoding="UTF8")
d = {}
print("anger,fear,joy,sadness,confident,analytical,tentative")
for i in file.readlines():
    x = {
        "text": i
    }
    response = requests.post(
        'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/9decad53-7281-4d48-8c86-f105d1f42122/v3/tone?version=2017-09-21',
        headers=headers, data=json.dumps(x), auth=('apikey', '2iYKycgYjL44PY1mo2F2Tcz_fTkM0YTip2pHh2tLl9q5'))
    anger = 0
    fear = 0
    joy = 0
    sadness = 0
    confident = 0
    tentative = 0
    analytical = 0
    for responses in response.json()['document_tone']['tones']:
        d[str(responses['tone_id'])] = responses['score']
        print(d)
        if responses['tone_id'] == 'anger':
            anger += responses['score']
        elif responses['tone_id'] == 'fear':
            fear += responses['score']
        elif responses['tone_id'] == 'joy':
            joy += responses['score']
        elif responses['tone_id'] == 'sadness':
            sadness += responses['score']
        elif responses['tone_id'] == 'confident':
            confident += responses['score']
        elif responses['tone_id'] == 'tentative':
            tentative += responses['score']
        else:
            analytical += responses['score']
        print(str(anger) + ',' + str(fear) + ',' + str(joy) + ',' + str(sadness), ','
              + str(confident) + ',' + str(analytical) + ',' + str(tentative))