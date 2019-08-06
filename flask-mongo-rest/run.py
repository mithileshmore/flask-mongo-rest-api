from flask import Flask
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
import json

client = MongoClient('localhost:27017')
db = client.ContactDB

app = Flask(__name__)

def rep(__self__):
    db.Format.Contact

@app.route("/add_contact", methods = ['POST'])
def add_contact():
    try:
        data = json.loads(request.data)
        user_name = data['name']
        user_contact = data['contact']
        if user_name and user_contact:
            status = db.Contacts.insert_one({
                "name" : user_name,
                "contact" : user_contact
            })
        print(status)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route("/get_all_contact", methods = ['GET'])
def get_all_contact():
    try:
        contacts = db.Contacts.find()
        # print(contacts.name)
        return dumps(contacts)
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route("/get_one_contact/<name>", methods = ['GET'])
def get_one_contact(name):
    try:
        x = db.Contacts.find_one({"name": name})
        return dumps(x)
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route("/update_one_contact/<name>", methods = ['PUT'])
def update_one_contact(name):
    try:
        data = json.loads(request.data)
        x = db.Contacts.find_one({"name": name})
        myquery = { "name": x['name'], "contact": x['contact'] }
        newvalues = { "$set": { "name": data["name"], "contact": data["contact"] } }
        status = db.Contacts.update_one(myquery, newvalues)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route("/delete_one_contact/<name>", methods = ['DELETE'])
def delete_one_contact(name):
    try:
        x = db.Contacts.find_one({"name": name})
        status = db.Contacts.delete_one(x)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route("/")
def home():
    return "Welcome!"

if(__name__=="__main__"):
    app.run(debug=True)