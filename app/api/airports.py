from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel  # Adicionado BaseModel
from sqlalchemy.orm import Session
from app.models.models import Airport, Flight
from app.database import get_db
from sqlalchemy import func

router = APIRouter()

# --- Models Pydantic ---
class OriginRequest(BaseModel):
    origin_code: str

# --- Endpoints ---
@router.get("/airports")
async def get_airports(db: Session = Depends(get_db)):
    airports = db.query(Airport).all()
    return [{"code": a.code, "name": a.name, "city": a.city} for a in airports]

@router.post("/airports-by-origin")
async def airports_by_origin(request: OriginRequest, db: Session = Depends(get_db)):
    origin_airport = db.query(Airport).filter(Airport.code == request.origin_code).first()
    if not origin_airport:
        raise HTTPException(status_code=404, detail="Aeroporto de origem não encontrado")
    
    flights = db.query(Flight).filter(Flight.origin_id == origin_airport.id).all()
    destination_ids = [f.destination_id for f in flights]
    
    airports = db.query(Airport).filter(Airport.id.in_(destination_ids)).all()
    return [{"code": a.code, "name": a.name} for a in airports]