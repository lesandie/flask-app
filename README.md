# README

## simple server with flask


```bash
curl -d '{ "dateOfBirth": "YY-MM-DD" }' -H 'Content-Type: application/json' -X PUT http://localhost:8080/hello/username
curl http://localhost:8080/hello/username
```

```sql
CREATE TABLE bday (
        id_user serial NOT NULL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        birthday date NOT NULL
);
```