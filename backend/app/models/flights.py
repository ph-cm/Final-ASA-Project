from app import db

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    origem = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    bookings = db.relationship("Booking", backref="flight", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "origem": self.origem,
            "destino": self.destino,
            "horario": self.horario
        }
