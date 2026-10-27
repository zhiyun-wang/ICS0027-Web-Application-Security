import json
import os

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_key(password, salt):
    return hash_secret_raw(
        password.encode('utf-8'),
        bytes(salt),
        time_cost=3,
        memory_cost=65536,
        parallelism=2,
        hash_len=32,
        type=Type.ID
    )


def encrypt(password, salt, username, account_password, owner_id):
    key = derive_key(password, salt)

    nonce = os.urandom(12)

    data = json.dumps({
        'username': username,
        'password': account_password
    }).encode('utf-8')

    ciphertext = AESGCM(key).encrypt(
        nonce,
        data,
        str(owner_id).encode()
    )

    return nonce, ciphertext


def decrypt(password, salt, nonce, ciphertext, owner_id):
    key = derive_key(password, salt)

    data = AESGCM(key).decrypt(
        bytes(nonce),
        bytes(ciphertext),
        str(owner_id).encode()
    )

    return json.loads(data.decode('utf-8'))