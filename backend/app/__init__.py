from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuração do banco PostgreSQL (ajuste os dados conforme seu ambiente)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@db:5432/nome_do_banco'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Registro dos blueprints
    from app.routes.users import users_bp
    from app.routes.flights import flights_bp
    from app.routes.bookings import bookings_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(flights_bp, url_prefix="/flights")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")

    # Criar as tabelas no banco
    with app.app_context():
        from app import models  # Importa os modelos para criar tabelas
        db.create_all()

    return app
