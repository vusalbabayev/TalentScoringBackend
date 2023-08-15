import environ, os, ast

from cryptography.fernet import Fernet

def decrypt_string(encrypted_data):
    env = environ.Env()
    environ.Env.read_env()
    hash_key = ast.literal_eval(env("hash_key"))
    cipher = Fernet(hash_key)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data.decode()