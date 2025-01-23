import hashlib


def hash_password(password):
    """Cria um hash seguro da senha usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()