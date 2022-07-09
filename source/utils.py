import hashlib

from source.settings import settings


def generate_random_hash(target_str: str) -> str:
    hash_object = hashlib.sha512(target_str.encode())
    hash_hex = hash_object.hexdigest()

    return hash_hex[0:settings.FILE_PATH_LENGTH]


def generate_short_url_based_on_hash(given_hash: str) -> str:
    return f'{settings.HOST}{given_hash}'
