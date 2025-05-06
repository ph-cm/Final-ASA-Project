from FinalASAProject.backend import db
from __init__ import d

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    bookings = db.relationship("Booking", backref="user", lazy=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}
