
import base64
import os

def encrypt(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

def decrypt(encrypted: str) -> str:
    return base64.b64decode(encrypted.encode()).decode()
