#! python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import sqlite3, os, random, string
import src.misc.config as global_config_variables

print("Welcome to the database initialization script.")
db_path = (global_config_variables.CONFIG["project_tree"]["root"]["subdirectories"]["assets"]["subdirectories"]
                                         ["data"]["directory"] +
           global_config_variables.CONFIG["project_tree"]["root"]["subdirectories"]["assets"]["subdirectories"]
                                         ["data"]["files"][1])
print(db_path)
with sqlite3.connect(db_path) as db_connection:
    print("Successfully connected to database!")
    db_handler = db_connection.cursor()
    username = None
    password = None
    salt = os.urandom(16)
    pepper = random.choice(list(string.ascii_letters))

    print("Warning: Please use only ASCII default characters...")
    try:
        username = input("Type in a username to be registered:")
        username = username.encode('ascii')
        password = input("Type in a password to be registered:")
        password += pepper
        password = password.encode('ascii')
    except UnicodeEncodeError:
        exit(1)

    print("Creating record...")
    key_base = PBKDF2HMAC(hashes.SHA256(), 32, salt, 10**5)
    key = key_base.derive(password)
    AES_handler = AES.new(key, AES.MODE_ECB)
    encrypted_pwd = AES_handler.encrypt(pad(password, AES.block_size))
    insertion_query = "INSERT INTO USERS (USERNAME, SALT, PASSWORD) VALUES (?,?,?)"
    db_handler.execute(insertion_query, (username, salt, encrypted_pwd))
    db_connection.commit()
