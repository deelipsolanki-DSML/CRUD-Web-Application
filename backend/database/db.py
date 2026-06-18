import sqlite3 as sq

error = None

def connect():  #try connecting to the database
    global error
    try:
        conn = sq.connect('database\data.db', check_same_thread = False)
        cur = conn.cursor()
        return cur, conn
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        return None, None

cur, conn = connect()

def read(qr):  # read operation

    cur.execute(qr)
    rows = cur.fetchall()
    return rows  # gives a list of tuples


def write(qr):
        cur.execute(qr)
        conn.commit()

def delete(id):

    cur.execute(f'''
    delete from users
    where id = '{id}'
                ''')
    conn.commit()


def update(qr, params):
    cur.execute(qr, params)
    conn.commit()

