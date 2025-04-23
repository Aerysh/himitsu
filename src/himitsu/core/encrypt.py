import os

from cryptography.fernet import Fernet

from himitsu.modules.derive_key import derive_key
from himitsu.modules.generate_salt import generate_salt


def encrypt_file(directory: str, password: str):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if not os.path.isfile(file_path):
            continue

        salt = generate_salt()
        key = derive_key(password, salt)
        fernet = Fernet(key)

        with open(file_path, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open(file_path, "wb") as encrypted_file:
            encrypted_file.write(salt + encrypted)
