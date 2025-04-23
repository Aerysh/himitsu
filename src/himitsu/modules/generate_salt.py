import os


def generate_salt():
    return os.urandom(16)
