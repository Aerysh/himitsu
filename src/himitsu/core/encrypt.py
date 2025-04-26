import base64
import os

from cryptography.fernet import Fernet

from himitsu.modules.derive_key import derive_key
from himitsu.modules.generate_salt import generate_salt


def encrypt_data(data: bytes, fernet: Fernet, salt: bytes) -> bytes:
    encrypted_data = fernet.encrypt(data)

    return salt + encrypted_data


def encrypt_filename(filename: str, salt: bytes, fernet: Fernet) -> str:
    encrypted_with_salt = encrypt_data(filename.encode("utf-8"), fernet, salt)

    return base64.urlsafe_b64encode(encrypted_with_salt).decode()


def encrypt_file(file_path: str, salt: bytes, fernet: Fernet):
    with open(file_path, "rb") as file:
        original = file.read()

    encrypted_with_salt = encrypt_data(original, fernet, salt)

    with open(file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_with_salt)


def process_file(file_path: str, password: str) -> None:
    salt = generate_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)

    encrypt_file(file_path, salt, fernet)

    original_filename = os.path.basename(file_path)
    encrypted_filename = encrypt_filename(original_filename, salt, fernet)

    new_path = os.path.join(os.path.dirname(file_path), encrypted_filename)
    os.rename(file_path, new_path)

    print(f"Successfully encrypted {new_path}")


def encrypt_directory(directory: str, password: str):
    for root, _, files in os.walk(directory, topdown=True):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                process_file(file_path, password)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue
