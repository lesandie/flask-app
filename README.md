# Simple web application example and deployment to public cloud

## Rationale

1. A simple "Hello World" application that exposes the following HTTP-based APIs:

* Description: Saves/updates the given user’s name and date of birth in the database.
        * Request: PUT /hello/<username> { “dateOfBirth”: “YYYY-MM-DD” }
        * Response: 204 No Content
        * Note:
                * <username> must contain only letters.
                * YYYY-MM-DD must be a date before the today date.

* Description: Returns hello birthday message for the given user
        * Request: Get /hello/<username>
        * Response: 200 OK
        * Response Examples:
                * A. If username’s birthday is in N days:
{ “message”: “Hello, <username>! Your birthday is in N day(s)”
}
                * B. If username’s birthday is today:
{ “message”: “Hello, <username>! Happy birthday!” }

2. For the database I'll use PostgreSQL. This cluster must be highly available
in case one zone goes down and even in case a whole region goes down due to a natural
disaster (tip: if you have proper automation backup and recovery in failover region could
be an option) - Using managed solution is not allowed
3. Produce a system diagram of your solution deployed to either AWS or GCP (it's not
required to support both cloud platforms).
4. Write configuration scripts for building and no-downtime production deployment of
this application, keeping in mind aspects that an SRE would have to consider.

Implicit requirements:
1. The code produced by you is expected to be of high quality.
2. The solution must have tests, runnable locally, and deployable to the cloud.


## Hello app

The app is located in the hello folder. To test it locally there are some requirements to be met:

* Install PostgreSQL and spin up an instance. Be sure that it listens in 0.0.0.0 or ::1

* Create a test database with the credentials you want

* Create a table as shown below: 

```sql
CREATE TABLE bday (
        id_user serial NOT NULL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        birthday date NOT NULL
);
```

* Create a Python virtualenv (3.8 or 3.9), you can use pyenv.

* Install the requirements:

```bash
(virtualenv)$ pip install -r hello/requirements.txt
```

* export the needed ENV variables. Have a look at the env file and change them according to your preferences:

```bash
(virtualenv)$ source ./env.sh
```

* Launch in a new terminal the Flask app:

```bash
(virtualenv)$ python hello/helloapp.py
```

* To test the app simple use curl and change the dateOfBirth and username:

```bash
(virtualenv)$ curl -d '{ "dateOfBirth": "YY-MM-DD" }' -H 'Content-Type: application/json' -X PUT http://localhost:8080/hello/username
(virtualenv)$ curl http://localhost:8080/hello/username
```

* There are some tests designed with Pytest. To use them open a new terminal:

```bash
(virtualenv)$ source ./env.sh
(virtualenv)$ pytest ./tests/tests.py
```

## PostgreSQL Cluster