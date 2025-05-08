# app/models/models.py (usando SQLAlchemy)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime)
    sessions = relationship("Session", back_populates="user")

class Session(Base):
    __tablename__ = "sessions"
    session_key = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String(45))
    expires_at = Column(DateTime)
    user = relationship("User", back_populates="sessions")

class Airport(Base):
    __tablename__ = "airports"
    id = Column(Integer, primary_key=True)
    code = Column(String(3), unique=True)
    name = Column(String(255))
    city = Column(String(255))
    country = Column(String(255))

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True)
    origin_id = Column(Integer, ForeignKey("airports.id"))
    destination_id = Column(Integer, ForeignKey("airports.id"))
    departure_time = Column(DateTime)
    price = Column(Numeric(10, 2))
    available_seats = Column(Integer)
    origin = relationship("Airport", foreign_keys=[origin_id])
    destination = relationship("Airport", foreign_keys=[destination_id])

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))
    passengers = Column(Integer)
    booking_ref = Column(String(6), unique=True)
    ticket_numbers = Column(JSON)
    created_at = Column(DateTime)