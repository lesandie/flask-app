import sys
sys.path.append("/home/dnieto/Repos/flask-app/hello")
import requests
import json
import os
from helloapp import *
from database import *

db_params = {
        'db': os.environ.get("PGDB"),
        'user': os.environ.get("PGUSER"),
        'pass': os.environ.get("PGPASS"),
        'host': os.environ.get("PGHOST"),
        'port': os.environ.get("PGPORT")
    }

def test_database():
    """
    Test if database is online and configured
    """
    result = connect_postgres(db_params)
    if result == False:
        assert False
    else:
        assert True

def test_add_username():
    """
    Test adding a username
    """
    data = {'dateOfBirth': '1971-01-01'}

    #headers = {'Content-type': 'application/json'}
    #HTTP methods in the requests library have a json parameter that will perform json.dumps() 
    #and set the Content-Type header to application/json:
    # Instead of response = requests.put(url, data=data, headers=headers)
    url = f"""http://localhost:{os.environ.get("PORT")}/hello/test"""
    # send PUT request
    response = requests.put(url, json=data)
    if response.status_code != 204:
        print(response.content)
        assert False
    else:
        assert True
