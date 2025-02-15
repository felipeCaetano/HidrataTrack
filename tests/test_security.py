import hashlib
from models.security import hash_password   # NoQA

def test_hash_password():
    """Testa se a função hash_password gera hashes corretos e consistentes."""
    
    password = "senha_segura"
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)

    # Verificar se o hash tem o tamanho esperado (64 caracteres para SHA-256)
    assert len(hashed1) == 64

    # Verificar se o mesmo input gera sempre o mesmo hash
    assert hashed1 == hashed2

    # Verificar se senhas diferentes geram hashes diferentes
    assert hash_password("outra_senha") != hashed1

    # Verificar se o hash é realmente um SHA-256 válido
    expected_hash = hashlib.sha256(password.encode()).hexdigest()
    assert hashed1 == expected_hash