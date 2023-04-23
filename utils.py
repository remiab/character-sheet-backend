from config import HOST, USER, PASSWORD
import mysql.connector
from PIL import Image
from io import BytesIO
from base64 import encodebytes

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


def get_from_db(db_name, query):
    try:
        db_connection = db_connect(db_name)
        cur = db_connection.cursor(dictionary=True)
        print(f"Connected to DB: {db_name.upper()}")

        cur.execute(query)
        result = cur.fetchall()
        cur.close()

    except Exception:
        raise DbConnectionError(f"Failed to read data from {db_name.upper()}")
    
    finally:
        if db_connection:
            db_connection.close()
            print(f"Connection to {db_name.upper()} is closed")
    return result


def update_prepared_status(db_name, query):
    
    try:
        db_connection = db_connect(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name.upper()}")

        cur.execute(query)
        db_connection.commit()
        print("committed")
        cur.close()

    except Exception:
        raise DbConnectionError(f"Failed to read data from {db_name.upper()}")
    
    finally:
        if db_connection:
            db_connection.close()
            print(f"Connection to {db_name.upper()} is closed")


def retrieve_spell_image(image_path):
    img = Image.open(image_path, mode='r')
    byte_arr = BytesIO()
    img.save(byte_arr, format='PNG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img


if __name__ == '__main__':
    get_from_db('ttrpg', 'CALL view_ithen_spells();')
