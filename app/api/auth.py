# app/api/auth.py
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, Request, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.models import Session as SessionModel, User
from app.database import get_db
from app.utils.auth_utils import (
    hash_password,
    verify_password,
    generate_session_key
)

router = APIRouter()

# ======================================
#           MODELOS PYDANTIC
# ======================================
class LoginRequest(BaseModel):
    email: str
    password: str

class LogoutRequest(BaseModel):
    session_key: str

class ValidateRequest(BaseModel):
    session_key: str
    ip_address: str

# ======================================
#           DEPENDÊNCIAS
# ======================================
def get_client_ip(request: Request) -> str:
    """Obtém o IP real do cliente (considerando proxies como Nginx)."""
    if "x-forwarded-for" in request.headers:
        return request.headers["x-forwarded-for"].split(",")[0]
    return request.client.host or "127.0.0.1"

# ======================================
#           ENDPOINTS
# ======================================
@router.post("/login")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
    client_ip: str = Depends(get_client_ip)
):
    """
    Efetua login e retorna uma chave de sessão.
    """
    # 1. Verifica se o usuário existe
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # 2. Valida a senha
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # 3. Gera uma nova sessão
    session_key = generate_session_key()
    expires_at = datetime.now() + timedelta(hours=24)  # Sessão expira em 24h

    new_session = SessionModel(
        session_key=session_key,
        user_id=user.id,
        ip_address=client_ip,
        expires_at=expires_at
    )

    db.add(new_session)
    db.commit()

    return {
        "session_key": session_key,
        "expires_at": expires_at.isoformat()
    }

@router.post("/logout")
async def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db)
):
    """
    Encerra uma sessão ativa.
    """
    session = db.query(SessionModel).filter(SessionModel.session_key == request.session_key).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    
    db.delete(session)
    db.commit()

    return {"message": "Logout realizado com sucesso"}

@router.post("/validate-session")
async def validate_session(
    request: ValidateRequest,
    db: Session = Depends(get_db)
):
    """
    Valida se uma sessão é ativa e está associada ao IP correto.
    """
    session = db.query(SessionModel).filter(SessionModel.session_key == request.session_key).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    
    if session.expires_at < datetime.now():
        raise HTTPException(status_code=401, detail="Sessão expirada")
    
    if session.ip_address != request.ip_address:
        raise HTTPException(status_code=403, detail="Acesso não autorizado (IP inválido)")
    
    return {
        "valid": True,
        "user_id": session.user_id,
        "expires_at": session.expires_at.isoformat()
    }