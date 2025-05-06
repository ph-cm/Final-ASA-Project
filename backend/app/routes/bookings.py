from flask import Blueprint, jsonify, request

bookings_bp = Blueprint("bookings", __name__)

# Simulação de banco de dados em memória
bookings_db = [
    {"id": 1, "user_id": 1, "flight_id": 1, "assento": "12A"},
    {"id": 2, "user_id": 2, "flight_id": 2, "assento": "14C"}
]

# Função auxiliar para buscar reserva por ID
def find_booking(booking_id):
    return next((b for b in bookings_db if b["id"] == booking_id), None)

# GET /bookings - listar todas as reservas
@bookings_bp.route("/", methods=["GET"])
def get_bookings():
    return jsonify(bookings_db), 200

# GET /bookings/<id> - buscar uma reserva por ID
@bookings_bp.route("/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = find_booking(booking_id)
    if booking:
        return jsonify(booking), 200
    return jsonify({"error": "Reserva não encontrada"}), 404

# POST /bookings - criar uma nova reserva
@bookings_bp.route("/", methods=["POST"])
def create_booking():
    data = request.get_json()
    if not data.get("user_id") or not data.get("flight_id") or not data.get("assento"):
        return jsonify({"error": "Campos 'user_id', 'flight_id' e 'assento' são obrigatórios"}), 400

    new_id = max(b["id"] for b in bookings_db) + 1 if bookings_db else 1
    new_booking = {
        "id": new_id,
        "user_id": data["user_id"],
        "flight_id": data["flight_id"],
        "assento": data["assento"]
    }
    bookings_db.append(new_booking)
    return jsonify(new_booking), 201

# PUT /bookings/<id> - atualizar uma reserva
@bookings_bp.route("/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    booking = find_booking(booking_id)
    if not booking:
        return jsonify({"error": "Reserva não encontrada"}), 404

    data = request.get_json()
    booking["user_id"] = data.get("user_id", booking["user_id"])
    booking["flight_id"] = data.get("flight_id", booking["flight_id"])
    booking["assento"] = data.get("assento", booking["assento"])
    return jsonify(booking), 200

# DELETE /bookings/<id> - remover uma reserva
@bookings_bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    booking = find_booking(booking_id)
    if not booking:
        return jsonify({"error": "Reserva não encontrada"}), 404

    bookings_db.remove(booking)
    return jsonify({"message": "Reserva removida com sucesso"}), 200
