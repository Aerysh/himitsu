import base64
import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

from himitsu.modules.derive_key import derive_key


def extract_salt_and_data(encrypted_data: bytes) -> tuple[bytes, bytes]:
    salt = encrypted_data[:16]
    data = encrypted_data[16:]

    return salt, data


def get_fernet(password: str, salt: bytes) -> Fernet:
    key = derive_key(password, salt)
    return Fernet(key)


def decrypt_filename(encrypted_filename: str, password) -> str:
    encrypted = base64.urlsafe_b64decode(encrypted_filename.encode("utf-8"))
    salt, filename_data = extract_salt_and_data(encrypted)

    fernet = get_fernet(password, salt)

    decrypted = fernet.decrypt(filename_data)

    return decrypted.decode("utf-8")


def decrypt_file(file_path: Path, password: str) -> None:
    with open(file_path, "rb") as encrypted_file:
        encrypted_with_salt = encrypted_file.read()

    salt, encrypted_content = extract_salt_and_data(encrypted_with_salt)
    fernet = get_fernet(password, salt)
    decrypted = fernet.decrypt(encrypted_content)

    with open(file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted)


def process_decryption(file_path: Path, root_dir: Path, password: str) -> None:
    decrypt_file(file_path, password)

    encrypted_filename = file_path.name
    decrypted_filename = decrypt_filename(encrypted_filename, password)

    relative_path = file_path.parent.relative_to(root_dir)
    new_path = root_dir / relative_path / decrypted_filename

    file_path.rename(new_path)
    print(f"Successfully decrypted {new_path}")


def decrypt_directory(directory: str, password: str):
    root_dir = Path(directory).resolve()
    for root, _, files in os.walk(directory, topdown=True):
        for filename in files:
            file_path = Path(root) / filename

            try:
                process_decryption(file_path, root_dir, password)
            except InvalidToken:
                print(
                    f"Decryption failed for {file_path} (wrong password or corrupted file)"
                )
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue
