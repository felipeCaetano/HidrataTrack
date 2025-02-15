import bcrypt
from typing import Tuple


def hash_password(password: str) -> str:
    """Cria um hash seguro da senha usando bcrypt.
    Args: password: A senha em texto puro
    Returns: str: Hash da senha em formato string"""
    
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verifica se uma senha corresponde ao hash armazenado.
    Args:   password: A senha em texto puro para verificar
            hashed: O hash armazenado para comparação
    Returns:
            bool: True se a senha corresponde ao hash, False caso contrário"""
    
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def password_meets_requirements(password: str) -> Tuple[bool, str]:
    """Verifica se a senha atende aos requisitos mínimos de segurança.
    Args: password: A senha a ser verificada
    Returns: Tuple[bool, str]: (True se válida, None)
            ou (False, mensagem de erro)"""
    
    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"
        
    if not any(c.isupper() for c in password):
        return False, "A senha deve conter pelo menos uma letra maiúscula"
        
    if not any(c.islower() for c in password):
        return False, "A senha deve conter pelo menos uma letra minúscula"
        
    if not any(c.isdigit() for c in password):
        return False, "A senha deve conter pelo menos um número"
        
    if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
        return False, "A senha deve conter pelo menos um caractere especial"
        
    return True, ""
