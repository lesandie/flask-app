import psycopg2
import os

def main():
    """
       Initialization of PostgreSQL: db_params = {'host':, 'port':, 'user':, 'pass':, 'db':}
    """
    #db params for the service container in github actions
    db_params = {
        'db': 'postgres',
        'user': 'postgres',
        'pass': os.environ.get("POSTGRES_PASSWORD"),
        'host': 'localhost',
        'port': '5432'
    }
    
    try:
        pg_pool = psycopg2.connect(f"dbname={db_params['db']} user={db_params['user']} password={db_params['pass']} host={db_params['host']} port={db_params['port']}")
        if(pg_pool):
            print("PostgreSQL connection created")
            with pg_pool.cursor() as cursor:
                query = f"CREATE TABLE bday (id_user serial NOT NULL PRIMARY KEY, username VARCHAR(50) NOT NULL, birthday date NOT NULL"
                cursor.execute(query)
                query = f"INSERT INTO bday (username, birthday) VALUES ('test', to_timestamp('1970-01-01', 'YYYY-MM-DD'));"
                cursor.execute(query)
                pg_pool.commit()
                print("Initialization complete")
                assert True
        print("PostgreSQL connection closed")
    except(Exception, psycopg2.DatabaseError) as error:
        print(f"Error while connecting and executing statements in PostgreSQL: {error}")
        assert False

if __name__ == "__main__":
    main()