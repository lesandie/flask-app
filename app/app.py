#!/usr/bin/env python3

"""
FLASK_APP=simple_flask_server.py flask run -h 127.0.0.1
"""

from flask import Flask, request, jsonify
import sys, os
from datetime import datetime
from database import *
import time

app = Flask(__name__)

db_params = {
        'db': 'test',
        'user': 'test',
        'pass': 'test',
        'host': 'localhost',
        'port': '5432'
    }

@app.route('/')
def hello():
    return "hello"


@app.route('/hello/<username>', methods=['PUT'])
def adduser(username):
    # a multidict containing POST data
    content = request.json
    put_data(username, content['dateOfBirth'], db_params)
    return "", 204

@app.route('/hello/<username>', methods=['GET'])
def getuser(username):
    date = get_data(username, db_params)
    if date is None:
        not_found = f"{username} not found"
        return jsonify(message=not_found)
    else:

        tday = datetime.today()
        bday = datetime.strptime(date, '%Y-%m-%d')
        if tday == bday:
            bday_is = f"Hello! {username} Happy Birthday!"
            return jsonify(message=bday_is)
        elif tday < bday:
            delta = bday - tday
            bday_is = f"Hello! {username} your bday is in {delta.days} days"
            return jsonify(message=bday_is)
        else:
            delta = tday - bday
            bday_is = f"Hello! {username} your bday is in {delta.days} days"
            return jsonify(message=bday_is)
             
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))