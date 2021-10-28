from flask import Flask
from flask import request
from flask import jsonify
from flask_pymongo import pymongo
from bson import json_util
import json

app = Flask(__name__)

CONNECTION_STRING = "mongodb+srv://andres:fernando22!@cluster0.vpba6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')


@app.route("/")
def test():
    user_collection.insert_one({"name": "John"})
    return "Connected to the data base!"

@app.route("/list")
def list():
    users = user_collection.find()
    response=[user for user in users]
    return json.dumps(response, default=json_util.default)

