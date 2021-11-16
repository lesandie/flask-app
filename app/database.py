import psycopg2

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
        put data into postgres
    """ 
    query = f"INSERT INTO bday (username, birthday) VALUES ('{username}', to_timestamp('{bday}', 'YYYY-MM-DD'));"
    conn = connect_postgres(db_params)
    with conn.cursor() as cursor:
        cursor.execute(query)
        # Important to commit the COPY or any other UPSERT/DELETE
        conn.commit()
        print("PostgreSQL connection closed")

def get_data(username, db_params: dict):
    query = f"SELECT to_char(birthday, 'YYYY-MM-DD') AS bday FROM bday WHERE username = '{username}';"
    conn = connect_postgres(db_params)
    with conn.cursor() as cursor:
        cursor.execute(query)
        # Important to commit the COPY or any other UPSERT/DELETE
        conn.commit()
        if cursor.rowcount == 0:
            print("PostgreSQL connection closed")
            return None
        else:
            data = cursor.fetchone()
            print("PostgreSQL connection closed")
            return data[0]
