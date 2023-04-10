from config import HOST, USER, PASSWORD
import mysql.connector

class DbConnectionError(Exception):
    pass


def db_connect(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin= 'mysql_native_password',
        database=db_name
    )
    return cnx


def get_spell_list():
    db_name = 'ttrpg'
    try:
        db_connection = db_connect(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name.upper()}")

        query = "CALL view_ithen_spells()"

        cur.execute(query)

        result = cur.fetchall()
        print(result)

        cur.close()

    except Exception:
        raise DbConnectionError(f"Failed to read data from {db_name.upper()}")
    
    finally:
        if db_connection:
            db_connection.close()
            print(f"Connection to {db_name.upper()} is closed")
    return result

if __name__ == '__main__':
    get_spell_list()
