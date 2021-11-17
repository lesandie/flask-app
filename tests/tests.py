import sys
sys.path.append("./hello")
import requests
import json
import os
from helloapp import *
from database import *

db_params = {
    'db': os.environ.get("POSTGRES_DB"),
    'user': os.environ.get("POSTGRES_USER"),
    'pass': os.environ.get("POSTGRES_PASSWORD"),
    'host': os.environ.get("POSTGRES_HOST"),
    'port': os.environ.get("POSTGRES_PORT")
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
    url = f"""http://localhost:6000/hello/test"""
    # send PUT request
    response = requests.put(url, json=data)
    if response.status_code != 204:
        print(response.content)
        assert False
    else:
        assert True
