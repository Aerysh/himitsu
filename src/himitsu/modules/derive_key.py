import base64

from cryptography.hazmat.primitives.kdf.argon2 import Argon2id


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=3,
        lanes=4,
        memory_cost=2**16,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
