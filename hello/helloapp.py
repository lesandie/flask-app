#!/usr/bin/python3
"""
Flask birthday app for Revolut 
"""

from flask import Flask, request, jsonify
import sys
import os
import psycopg2
from datetime import datetime

# DB params that will be used to connect to the db
db_params = {
    'db': os.environ.get("POSTGRES_DB"),
    'user': os.environ.get("POSTGRES_USER"),
    'pass': os.environ.get("POSTGRES_PASSWORD"),
    'host': os.environ.get("POSTGRES_HOST"),
    'port': os.environ.get("POSTGRES_PORT")
    }

def connect_postgres(db_params: dict):
        """
            Connect to PostgreSQL: db_params = {'host':, 'port':, 'user':, 'pass':, 'db':}
            Returns a connection
        """
        try:
            pg_pool = psycopg2.connect(f"dbname={db_params['db']} user={db_params['user']} password={db_params['pass']} host={db_params['host']} port={db_params['port']}")
            if(pg_pool):
                print("PostgreSQL connection created")
                return pg_pool
        except(Exception, psycopg2.DatabaseError) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
            return False

def put_data(username, bday, db_params: dict):
    """
        Puts data (username and birthdate into postgres) 
    """ 
    query = f"INSERT INTO bday (username, birthday) VALUES ('{username}', to_timestamp('{bday}', 'YYYY-MM-DD'));"
    conn = connect_postgres(db_params)
    with conn.cursor() as cursor:
        cursor.execute(query)
        # Important to commit with any UPSERT/DELETE
        conn.commit()
        print("PostgreSQL connection closed")

def get_data(username, db_params: dict):
    """
        Returns the birthdate for a given username
    """
    query = f"SELECT to_char(birthday, 'YYYY-MM-DD') AS bday FROM bday WHERE username = '{username}';"
    conn = connect_postgres(db_params)
    with conn.cursor() as cursor:
        cursor.execute(query)
        # If no results then return None
        if cursor.rowcount == 0:
            print("PostgreSQL connection closed")
            return None
        else:
            # Fetch the first row (we could use here LIMIT 1)
            data = cursor.fetchone()
            print("PostgreSQL connection closed")
            return data[0]

### Flask app begin
app = Flask(__name__)

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
    app.run(debug=True, host="localhost", port=int(os.environ.get("PORT")))
