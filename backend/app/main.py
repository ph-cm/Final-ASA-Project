from flask import Flask
from app.routes.users import users_bp
from app.routes.flights import flights_bp
from app.routes.bookings import bookings_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(flights_bp, url_prefix="/flights")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
