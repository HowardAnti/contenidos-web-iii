
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models.usuario_model import User
from app.utils.decorators import jwt_required, roles_required
from app.views.user_view import render_user_list, render_user_detail


user_bp = Blueprint("usuario", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    roles = data.get("roles") 

    if not username or not password:
        return jsonify({"error": "Se requieren nombre de usuario y contraseña"}), 400

    existing_user = User.find_by_username(username)
    if existing_user:
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

    new_user = User(username, password, roles)
    new_user.save()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.find_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        # Si las credenciales son válidas, genera un token JWT
        access_token = create_access_token(
            identity={"username": username, "roles": user.roles}
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401



@user_bp.route("/usuarios", methods=["GET"])
@jwt_required
@roles_required(["admin"])
def get_users():
    users = User.get_all()
    return jsonify(render_user_list(users))



@user_bp.route("/usuario/<int:id>", methods=["GET"])
@jwt_required
@roles_required(["admin"])
def get_user(id):
    user = User.get_by_id(id)
    if user:
        return jsonify(render_user_detail(user))
    return jsonify({"Error": "user no encontrado"}),404
