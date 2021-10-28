from flask import Flask
from flask import request
from flask import jsonify
from flask_pymongo import pymongo
from bson import json_util
import ssl
import json
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CONNECTION_STRING = "mongodb+srv://andres:pruebatec@cluster0.zllxo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING,ssl_cert_reqs=ssl.CERT_NONE)
db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')
todo_collection = pymongo.collection.Collection(db, 'todo_collection')


@app.route("/")
def test():
    user_collection.insert_one({"name": "John"})
    return "Connected to the data base!"

@app.route("/list")
def list():
    users = user_collection.find()
    response=[user for user in users]
    return json.dumps(response, default=json_util.default)

@app.route("/create",methods=['POST'])
def create_user():
    data= request.json
    user_collection.insert_one({"_id":str(uuid.uuid4()),"name":data["name"],"last_name":data["last_name"]})
    return "User created"

@app.route("/find/<id>",methods=['GET'])
def get_by_id(id):
    user=user_collection.find_one({"_id":id})
    return json.dumps(user, default=json_util.default)

@app.route("/todo",methods=['POST'])
def create_todo():
    data=request.json
    todo_collection.insert_one({"_id":str(uuid.uuid4()),"task":data["task"],"done":False})
    return "Task created"

@app.route("/todo/list",methods=['GET'])
def list_todo():
    todos = todo_collection.find()
    response=[todo for todo in todos]
    return json.dumps(response, default=json_util.default)

@app.route("/todo/complete/<id>",methods=['GET'])
def update_todo(id):
    todo=todo_collection.update_one({"_id":id},{"$set":{"done":True}})
    return f"Task {id} completed"
