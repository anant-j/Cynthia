from flask import Flask, request
from pymongo import MongoClient
import json
import datetime
from bson.json_util import dumps

app = Flask(__name__)
client = MongoClient("mongodb+srv://admin:admin@cluster0-h7osn.mongodb.net/test?retryWrites=true&w=majority")
db = client['MsRogers']


@app.route('/stats', methods=["POST"])
def add_sentiment_value():
    response = {"date": datetime.datetime.utcnow(), "score": request.json["data"]}
    try:
        db.sentiments.insert_one(response)
    except:
        return json.dumps({"saved": False})
    return json.dumps({"saved": True})


@app.route('/stats', methods=["GET"])
def get_stats():
    limit_size = request.json["limit"]
    try:
        return dumps(list(db.sentiments.find().sort("date", -1).limit(limit_size)))
    except:
        return json.dumps({"response": False})


@app.route('/conversation', methods=["POST"])
def add_conversation():
    response = {"question": request.json["question"], "answer" : request.json["answer"]}
    try:
        db.conversation_log.insert_one(response)
    except:
        return json.dumps({"saved": False})
    return json.dumps({"saved": True})


@app.route('/conversation', methods=["GET"])
def get_conversation():
    limit_size = request.json["limit"]
    try:
        return dumps(list(db.conversation_log.find().sort("date", -1).limit(limit_size)))
    except:
        return json.dumps({"reponse": False})


if __name__ == "__main__":
    app.run()
