import json
import base64
from src.config import cipher_suite

def encrypt_data(data):
    json_str = json.dumps(data, default=str)
    encrypted = cipher_suite.encrypt(json_str.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_data(encrypted_data):
    encrypted_bytes = base64.b64decode(encrypted_data.encode())
    decrypted = cipher_suite.decrypt(encrypted_bytes)
    return json.loads(decrypted.decode())
