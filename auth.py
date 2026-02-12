import sqlite3
import hashlib


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False



conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()


def create_usertable():
    # Added 'role' column to the table creation
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT, role TEXT)')


def add_userdata(username, password, role):
    create_usertable()
    c.execute('INSERT INTO userstable(username,password,role) VALUES (?,?,?)', (username, password, role))
    conn.commit()


def login_user(username, password):
    create_usertable()
    hashed_pswd = make_hashes(password)
    # Modified to select based on username and password
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, hashed_pswd))
    data = c.fetchall()
    return data


def create_user(username, password, role="user"):
    # Check if user already exists
    create_usertable()
    c.execute('SELECT * FROM userstable WHERE username =?', (username,))
    if c.fetchall():
        return False  # User already exists

    hashed_pswd = make_hashes(password)
    add_userdata(username, hashed_pswd, role)
    return True