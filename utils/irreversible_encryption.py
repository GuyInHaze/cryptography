import hashlib

def hash_string(text: str, algorithm: str = "sha256") -> str:
    """
    Хеширует строку с выбранным алгоритмом.
    Доступные алгоритмы: md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s.
    """
    if algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Алгоритм {algorithm} не поддерживается!")
    
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode())
    return hasher.hexdigest()