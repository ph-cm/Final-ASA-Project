# app/api/bookings.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import secrets
from sqlalchemy.orm import Session
from app.models.models import Booking, Flight
from app.database import get_db
from app.api.dependencies import get_current_session  # Implemente esta função

router = APIRouter()

# --- Models Pydantic ---
class PurchaseRequest(BaseModel):
    session_key: str
    flight_id: int
    passengers: int

# --- Endpoints ---
@router.post("/purchase")
async def purchase(
    request: PurchaseRequest,
    db: Session = Depends(get_db),
    session: dict = Depends(get_current_session)  # Valida a sessão
):
    flight = db.query(Flight).filter(Flight.id == request.flight_id).first()
    if not flight or flight.available_seats < request.passengers:
        raise HTTPException(status_code=400, detail="Assentos insuficientes")
    
    booking_ref = secrets.token_hex(3).upper()
    ticket_numbers = [f"TKT-{secrets.token_hex(2).upper()}" for _ in range(request.passengers)]
    
    flight.available_seats -= request.passengers
    booking = Booking(
        user_id=session["user_id"],  # Obtido da sessão válida
        flight_id=request.flight_id,
        passengers=request.passengers,
        booking_ref=booking_ref,
        ticket_numbers=ticket_numbers,
        created_at=datetime.now()
    )
    db.add(booking)
    db.commit()
    
    return {
        "booking_ref": booking_ref,
        "tickets": ticket_numbers
    }