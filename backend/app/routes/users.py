from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__)

# Simulação de banco de dados em memória
users_db = [
    {"id": 1, "nome": "Alice", "email": "alice@email.com"},
    {"id": 2, "nome": "Bob", "email": "bob@email.com"}
]

# Função auxiliar para buscar usuário por ID
def find_user(user_id):
    return next((u for u in users_db if u["id"] == user_id), None)

# GET /users - listar todos
@users_bp.route("/", methods=["GET"])
def get_users():
    return jsonify(users_db), 200

# GET /users/<id> - buscar por ID
@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = find_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "Usuário não encontrado"}), 404

# POST /users - adicionar novo
@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("nome") or not data.get("email"):
        return jsonify({"error": "Campos 'nome' e 'email' são obrigatórios"}), 400

    new_id = max(u["id"] for u in users_db) + 1 if users_db else 1
    new_user = {
        "id": new_id,
        "nome": data["nome"],
        "email": data["email"]
    }
    users_db.append(new_user)
    return jsonify(new_user), 201

# PUT /users/<id> - atualizar
@users_bp.route("/<int:user_id>", methods=["."])
def update_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    data = request.get_json()
    user["nome"] = data.get("nome", user["nome"])
    user["email"] = data.get("email", user["email"])
    return jsonify(user), 200

# DELETE /users/<id> - remover
@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    users_db.remove(user)
    return jsonify({"message": "Usuário removido com sucesso"}), 200
