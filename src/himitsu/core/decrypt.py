import base64
import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

from himitsu.config import HEADER_LENGTH, MAGIC_BYTES, METADATA_LENGTH, VERSION
from himitsu.modules.derive_key import derive_key


def verify_and_extract_metadata(encrypted_data: bytes) -> tuple[bytes, bytes]:
    if len(encrypted_data) < METADATA_LENGTH:
        raise ValueError("Invalid encrypted file: file too short")

    magic = encrypted_data[: len(MAGIC_BYTES)]
    if magic != MAGIC_BYTES:
        raise ValueError("File is not a valid HIMITSU encrypted file")

    version = encrypted_data[len(MAGIC_BYTES)]
    if version != VERSION:
        raise ValueError(f"Unsupported encryption version: {version}")

    salt = encrypted_data[HEADER_LENGTH:METADATA_LENGTH]
    data = encrypted_data[METADATA_LENGTH:]

    return salt, data


def get_fernet(password: str, salt: bytes) -> Fernet:
    key = derive_key(password, salt)
    return Fernet(key)


def decrypt_filename(encrypted_filename: str, password: str) -> str:
    try:
        encrypted = base64.urlsafe_b64decode(encrypted_filename.encode("utf-8"))
        salt, filename_data = verify_and_extract_metadata(encrypted)
        fernet = get_fernet(password, salt)
        decrypted = fernet.decrypt(filename_data)
        return decrypted.decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to decrypt filename: {str(e)}")


def decrypt_file(file_path: Path, password: str) -> None:
    with open(file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    try:
        salt, encrypted_content = verify_and_extract_metadata(encrypted_data)
        fernet = get_fernet(password, salt)
        decrypted = fernet.decrypt(encrypted_content)
    except ValueError as e:
        raise ValueError(f"Decryption failed: {str(e)}") from e

    with open(file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted)


def process_decryption(file_path: Path, root_dir: Path, password: str) -> None:
    try:
        with open(file_path, "rb") as f:
            magic = f.read(len(MAGIC_BYTES))
            if magic != MAGIC_BYTES:
                print(f"Skipping {file_path}: not a HIMITSU encrypted file")
                return

        decrypt_file(file_path, password)

        encrypted_filename = file_path.name
        decrypted_filename = decrypt_filename(encrypted_filename, password)

        relative_path = file_path.parent.relative_to(root_dir)
        new_path = root_dir / relative_path / decrypted_filename

        file_path.rename(new_path)
        print(f"Successfully decrypted {new_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        raise


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
