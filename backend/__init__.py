from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .users import User
from .flight import Flight
from .booking import Booking

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuração do banco
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@db:5432/nome_do_banco'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importa e registra os blueprints
    from app.routes.users import users_bp
    from app.routes.flights import flights_bp
    from app.routes.bookings import bookings_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(flights_bp, url_prefix="/flights")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")

    # Importa os modelos para criar as tabelas
    with app.app_context():
        from app.models import User, Flight, Booking
        db.create_all()

    return app
