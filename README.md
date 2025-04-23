# himitsu

Simple and secure file encryption and decryption

## Features

- Argon2id key derivation
- Secure random numbers for salt

## Usage

Encryption

```bash

himitsu encrypt -p <directory>

```

Example:

```bash
himitsu encrypt -p /home/aerysh/Documents/secret
Enter encryption password:
```

Decryption

```bash
himitsu decrypt -p <directory>
```

Example:

```bash
himitsu decrypt -p /home/aerysh/Documents/secret
Enter decryption password:
```

## License

This project is licensed under [Mozilla Public License 2.0](https://github.com/Aerysh/himitsu?tab=MPL-2.0-1-ov-file)
