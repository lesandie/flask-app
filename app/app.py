#!/usr/bin/env python3

"""See flask.palletsprojects.com.  This used Flask 1.1.1.  Run with:
FLASK_APP=simple_flask_server.py flask run -h 127.0.0.1
"""

from flask import Flask, request
import sys, os


app = Flask(__name__)


records = {}


@app.route('/')
def hello():
    return "hello"


@app.route('/api/v1/addrecord/<name>', methods=['POST'])
def addrecord(name):
    # a multidict containing POST data
    print(f"records[{name}]={request.data}")
    records[name] = request.data
    return ""


@app.route('/api/v1/shutdown', methods=['GET'])
def shutdown():
    # See https://stackoverflow.com/a/17053522/34935
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
    shutdown_server()
    return "Shutting down"


@app.route('/api/v1/getrecord/<name>', methods=['GET'])
def getrecord(name):
    return records[name]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))