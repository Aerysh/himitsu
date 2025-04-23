import argparse
import getpass

from himitsu.core.decrypt import decrypt_file
from himitsu.core.encrypt import encrypt_file
from himitsu.modules.dir_path import dir_path


def main():
    parser = argparse.ArgumentParser(description="Himitsu")
    subparser = parser.add_subparsers(dest="command", required=True)

    encrypt_parser = subparser.add_parser("encrypt", help="Encrypt a directory")
    encrypt_parser.add_argument(
        "-p",
        "--path",
        type=dir_path,
        help="Path to directory to be encrypted",
        required=True,
    )

    decrypt_parser = subparser.add_parser("decrypt", help="Decrypt a directory")
    decrypt_parser.add_argument(
        "-p",
        "--path",
        type=dir_path,
        help="Path to directory to be decrypted",
        required=True,
    )

    args = parser.parse_args()

    if args.command == "encrypt":
        password = getpass.getpass("Enter encryption password: ")
        encrypt_file(args.path, password)

    elif args.command == "decrypt":
        password = getpass.getpass("Enter decryption password: ")
        decrypt_file(args.path, password)
