#!/usr/bin/python3
"""
Flask birthday app for Revolut 
"""

from flask import Flask, request, jsonify
import sys, os
from datetime import datetime
from database import *

app = Flask(__name__)

# DB params that will be used to connect to the db
db_params = {
        'db': os.environ.get("PGDB"),
        'user': os.environ.get("PGUSER"),
        'pass': os.environ.get("PGPASS"),
        'host': os.environ.get("PGHOST"),
        'port': os.environ.get("PGPORT")
    }

# test endpoint
@app.route('/')
def hello():
    return "hello"

# PUT endpoint
@app.route('/hello/<username>', methods=['PUT'])
def adduser(username):
    content = request.json
    put_data(username, content['dateOfBirth'], db_params)
    return "", 204

# GET endpoint
@app.route('/hello/<username>', methods=['GET'])
def getuser(username):
    # check in db for the username's birthday
    date = get_data(username, db_params)
    if date is None:
        not_found = f"{username} not found"
        return jsonify(message=not_found)
    else:
        # user found
        tday = datetime.today()
        bday = datetime.strptime(date, '%Y-%m-%d')
        # replace year
        bday = bday.replace(year=tday.year)
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
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT")))