# app/utils/auth_utils.py
import secrets
import bcrypt
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    """Gera um hash seguro da senha usando bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        if not hashed_password.startswith('$2b$'):
            print("Hash inválido! Deve começar com $2b$")
            return False
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        print(f"Erro na verificação: {str(e)}")
        return False

def generate_session_key() -> str:
    """Gera uma chave de sessão aleatória."""
    return secrets.token_urlsafe(32)  # Exemplo: 'aBcDeF123...'