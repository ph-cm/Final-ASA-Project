from flask import Blueprint, jsonify

flights_bp = Blueprint("flights", __name__)

@flights_bp.route("/", methods=["GET"])
def get_flights():
    return jsonify({"message": "Lista de voos disponíveis"})
