# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    auth,
    airports,
    flights,
    bookings
)
from app.database import Base, engine

# Cria as tabelas no banco de dados (apenas para desenvolvimento)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Companhia Aérea",
    description="API para gerenciamento de voos, aeroportos e reservas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os routers
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(airports.router, prefix="/airports", tags=["Aeroportos"])
app.include_router(flights.router, prefix="/flights", tags=["Voos"])
app.include_router(bookings.router, prefix="/bookings", tags=["Reservas"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao sistema da companhia aérea!"}