import os

from cryptography.fernet import Fernet, InvalidToken

from himitsu.modules.derive_key import derive_key


def decrypt_file(directory, password):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, "rb") as file:
            salt = file.read(16)
            encrypted = file.read()

        try:
            key = derive_key(password, salt)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted)

            with open(file_path, "wb") as file:
                file.write(decrypted)

        except InvalidToken:
            print(f"Failed to decrypt {filename} (wrong password or corrupted file)")
            continue
