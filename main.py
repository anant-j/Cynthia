from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['POST'])
def request():
    return 'this is a post request'


@app.route('/', methods=['GET'])
def receive():
    return 'this is get request'


if __name__ == '__main__':
    app.run()
