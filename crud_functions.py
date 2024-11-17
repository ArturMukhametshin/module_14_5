import sqlite3

from matplotlib.backend_bases import cursors


def initiate_db():
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER
    )
    ''')
    connection.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()
    

def get_all_products():
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()

    cursor.execute("SELECT title, description, price FROM Products")
    users = cursor.fetchall()

    connection.commit()
    return users
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect("shop.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users")
    total_us = cursor.fetchone()[0] + 1
    cursor.execute(f'''
        INSERT INTO Users VALUES('{total_us}', '{username}', '{email}', '{age}', '1000')
        ''')

    connection.commit()
    connection.close()
    

def is_included(username):
    connection = sqlite3.connect('shop.db')
    cursor = connection.cursor()
    is_inc = True
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    if check_user.fetchone() is None:
        is_inc = False
    connection.commit()
    return is_inc
    connection.close()


initiate_db()
