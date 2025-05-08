# app/api/dependencies.py
from fastapi import HTTPException, Depends, Header
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Session as SessionModel
from app.database import get_db

async def get_current_session(
    session_key: str = Header(..., alias="session-key"),
    ip: str = Header(..., alias="x-real-ip"),  # Use o header correto para IP
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.session_key == session_key).first()
    if not session or session.expires_at < datetime.now() or session.ip_address != ip:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    return {"user_id": session.user_id, "session_key": session_key}