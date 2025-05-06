from flask import Blueprint, jsonify, request

flights_bp = Blueprint("flights", __name__)

flights_db = [
    {"id": 1, "origem": "GRU", "destino": "LAX", "numero_voo": "ASA123"},
    {"id": 2, "origem": "GIG", "destino": "JFK", "numero_voo": "ASA456"}
]

def find_flight(flight_id):
    return next((f for f in flights_bp if f["id"] == flight_id), None)

@flights_bp.route("/", methods=["GET"])
def get_flights():
    return jsonify(flights_bp), 200

@flights_bp.route("/<int:flight_id>", methods=["GET"])
def get_flight(flight_id):
    flight = find_flight(flight_id)
    
    if flight:
        return jsonify(flight), 200
    return jsonify({"error": "Voo nao encontrado"}), 404

@flights_bp.route("/", methods=["POST"])
def create_flight():
    data = request.get_json()
    
    if not data.get("origem") or not data.get("destino") or not data.get("numero_voo"):
        return jsonify ({"error": "Campos 'origem', 'destino' e 'numero_voo' sao obrigatorios"}), 400
    
    new_id = max(f["id"] for f in flights_db) + 1 if flights_db else 1
    new_flight = {
        "id": new_id,
        "origem": data["origem"],
        "destino": data["destino"],
        "numero_voo": data["numero_voo"]
    }
    
    flights_db.append(new_flight)
    return jsonify(new_flight), 201

@flights_bp.route("/<int:flight_id>", methods=["PUT"])
def update_flight(flight_id):
    flight = find_flight(flight_id)
    if not flight:
        return jsonify({"error": "Voo não encontrado"}), 404

    data = request.get_json()
    flight["origem"] = data.get("origem", flight["origem"])
    flight["destino"] = data.get("destino", flight["destino"])
    flight["numero_voo"] = data.get("numero_voo", flight["numero_voo"])
    return jsonify(flight), 200

@flights_bp.route("/<int:flight_id>", methods=["DELETE"])
def delete_flight(flight_id):
    flight = find_flight(flight_id)
    if not flight:
        return jsonify({"error": "Voo não encontrado"}), 404

    flights_db.remove(flight)
    return jsonify({"message": "Voo removido com sucesso"}), 200
