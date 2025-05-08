# app/api/flights.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Flight, Airport
from app.database import get_db
from sqlalchemy import func

router = APIRouter()

# --- Models Pydantic ---
class FlightRequest(BaseModel):
    date: datetime

class SearchRequest(BaseModel):
    origin_code: str
    destination_code: str
    passengers: int
    date: datetime

# --- Endpoints ---
@router.post("/flights")
async def get_flights(request: FlightRequest, db: Session = Depends(get_db)):
    flights = db.query(Flight).filter(
        func.date(Flight.departure_time) == request.date.date()
    ).all()
    return [{
        "id": f.id,
        "origin": f.origin.code,
        "destination": f.destination.code,
        "departure": f.departure_time.isoformat(),
        "price": float(f.price)
    } for f in flights]

@router.post("/search-flights")
async def search_flights(request: SearchRequest, db: Session = Depends(get_db)):
    origin = db.query(Airport).filter(Airport.code == request.origin_code).first()
    destination = db.query(Airport).filter(Airport.code == request.destination_code).first()
    
    if not origin or not destination:
        raise HTTPException(status_code=404, detail="Aeroporto(s) não encontrado(s)")
    
    flights = db.query(Flight).filter(
        Flight.origin_id == origin.id,
        Flight.destination_id == destination.id,
        Flight.available_seats >= request.passengers,
        func.date(Flight.departure_time) == request.date.date()
    ).order_by(Flight.price).all()
    
    return [{
        "flight_id": f.id,
        "price": float(f.price),
        "seats_available": f.available_seats
    } for f in flights]