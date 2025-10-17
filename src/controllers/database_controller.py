#! python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import sqlite3, string, base64
from src.misc.config import CONFIG, DB_FILE_PATH

class DatabaseCtrl:

    def __init__(self):
        self.username = None
        self.password = None
        self.key = None
        self.salt = None
        self.authentication_validity = False
        self.database_path = DB_FILE_PATH

    def authenticate(self, username, password):
        self.username = username; self.password = password
        with sqlite3.connect(self.database_path) as database:
            SQLite3_handler = database.cursor()
            custom_query = f"SELECT * FROM USERS WHERE USERNAME IS \"{self.username}\""
            SQLite3_handler.execute(custom_query)
            raw_result = SQLite3_handler.fetchall()[0]
            if len(raw_result) != 0:
                self.salt = raw_result[2]
                encrypted_credentials = raw_result[3]
                pepper_possibilities = list(string.ascii_letters)
                for character in pepper_possibilities:
                    comparative_output_source = (self.password + character).encode('ascii')
                    iterations = CONFIG["security"]["pbkdf2_iterations"]
                    PBKDF2HMAC_encoder_handler = PBKDF2HMAC(hashes.SHA256(), 32, self.salt, iterations)
                    self.key = PBKDF2HMAC_encoder_handler.derive(comparative_output_source)
                    AES_encoder_handler = AES.new(self.key, AES.MODE_ECB)
                    comparative_output = AES_encoder_handler.encrypt(pad(comparative_output_source, AES.block_size))
                    if comparative_output == encrypted_credentials:
                        self.authentication_validity = True
                        self.password = comparative_output
                        return self.authentication_validity
            return False

    def get_decrypted_target_record(self, target_id):
        if self.authentication_validity:
            with sqlite3.connect(self.database_path) as database:
                SQLite3_handler = database.cursor()
                custom_query = f"SELECT * FROM RECORDS WHERE RECORD_ID IS \"{target_id}\""
                SQLite3_handler.execute(custom_query)
                raw_result = SQLite3_handler.fetchall()
                decryptor_key_handler = Fernet(base64.urlsafe_b64encode(self.key))
                decryptor_data_handler = Fernet(raw_result[0][3])
                decryptor = MultiFernet([decryptor_key_handler, decryptor_data_handler])
                source_record = list()
                for chunk in raw_result[0][-2:]:
                        source_record.append(decryptor.decrypt(chunk))
                return source_record
        else:
            return Exception("Error: failed to authenticate.")


    def encrypt_and_insert_record(self, record_description, record_username, record_password):
        if self.authentication_validity:
            with sqlite3.connect(self.database_path) as database:
                SQLite3_handler = database.cursor()
                custom_query = "INSERT INTO RECORDS (OWNER, DESCRIPTION, SALT, USERNAME, PASSWORD) VALUES (?,?,?,?,?)"
                raw_random_salt_source = Fernet.generate_key()
                raw_decryptor_key = Fernet(base64.urlsafe_b64encode(self.key))
                raw_decryptor_salt = Fernet(raw_random_salt_source)
                decryptor = MultiFernet([raw_decryptor_key,raw_decryptor_salt])
                encrypted_record_username = decryptor.encrypt(record_username.encode('ascii'))
                encrypted_record_password = decryptor.encrypt(record_password.encode('ascii'))
                SQLite3_handler.execute(custom_query, (self.username, record_description, raw_decryptor_salt, encrypted_record_username, encrypted_record_password))
                database.commit()
                return None
        else:
            return Exception("Error: failed to authenticate.")

    def get_all_records(self):
        if self.authentication_validity:
            with sqlite3.connect(self.database_path) as database:
                SQLite3Handler = database.cursor()
                custom_query = f"SELECT * FROM RECORDS WHERE OWNER IS \"{self.username}\""
                SQLite3Handler.execute(custom_query)
                record_list = list()
                for record_entry in SQLite3Handler.fetchall():
                    record_list.append(record_entry[:3])
                return record_list
        else:
            return Exception("Error: failed to authenticate.")

    def delete_target_record(self, target_id):
        if self.authentication_validity:
            with sqlite3.connect(self.database_path) as database:
                SQLite3_handler = database.cursor()
                custom_query = f"DELETE FROM RECORDS WHERE OWNER IS \"{self.username}\" AND RECORD_ID IS \"{target_id}\""
                SQLite3_handler.execute(custom_query)
                database.commit()
                return None
        else:
            return Exception("Error: failed to authenticate.")