import datetime
from flask import Flask, render_template,request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv('MONGO_DB_URI'))
    app.db = client.microblog

    @app.route("/", methods = ["GET","POST"])
    def render_index():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        
        entries_with_date = [
            (
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime('%b %d') 
            )
            for entry in app.db.entries.find({})
        ]

        return render_template('index.html',entries = entries_with_date)
    
    @app.route("/addUser", methods = ["POST"])
    def addUser():
        print(request.data)
        record = json.loads(request.data)
        app.db.user.insert_one({"device_id": record['device_id'], "mobile_no": record["mobile_no"]
                                , "country_code": record["country_code"], "app_id": record["app_id"]})
        print(record)
        return jsonify(record)

    return app