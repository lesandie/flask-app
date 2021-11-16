# README

## simple server with flask

```bash

./simple_server.py 7000 127.0.0.1
Example client calls and responses using httpie:

$ http -f POST http://127.0.0.1:7000/api/v1/addrecord/one Content-Type:application/json var1=value1 var2=value2
HTTP/1.0 200 OK
Date: Sun, 13 Oct 2019 18:02:15 GMT
Server: BaseHTTP/0.6 Python/3.7.4

$ http http://127.0.0.1:7000/api/v1/getrecord/one
HTTP/1.0 200 OK
Content-Type: application/json
Date: Sun, 13 Oct 2019 18:14:09 GMT
Server: BaseHTTP/0.6 Python/3.7.4
```

```json
{
    "var1": [
        "value1"
    ],
    "var2": [
        "value2"
    ]
}
```

```bash
$ http http://127.0.0.1:7000/api/v1/shutdown
HTTP/1.0 200 OK
Date: Sun, 13 Oct 2019 18:02:22 GMT
Server: BaseHTTP/0.6 Python/3.7.4
```

```bash
curl -d '{ "dateOfBirth": "YY-MM-DD" }' -H 'Content-Type: application/json' -X PUT http://localhost:8080/hello/username
```

```sql
CREATE TABLE bday (
        id_user serial NOT NULL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        birthday date NOT NULL
);
```