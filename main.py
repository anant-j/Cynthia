from flask import Flask
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def request():
    return 'this is a post request'


@app.route('/', methods=['GET'])
def receive():
    headers = {
        'Content-Type': 'application/json',
    }

    data = open('D:\\Downloads\\tone.json', 'rb').read()
    response = requests.post(
        'url',
        headers=headers, data=data, auth=('apikey', 'api'))
    return response.json()


if __name__ == '__main__':
    app.run()
