import hashlib


def generate_random_hash(target_str: str) -> str:
    hash_object = hashlib.sha512(target_str.encode())
    hash_hex = hash_object.hexdigest()

    return hash_hex[0:6]
