from flask import Blueprint, jsonify, request

from models.producto_model import Producto
from utils.decorators import jwt_required, roles_required
from views.producto_view import render_product_detail, render_product_list

# Crear un blueprint para el controlador de animales
producto_bp = Blueprint("producto", __name__)


# Ruta para obtener la lista de animales
@producto_bp.route("/productos", methods=["GET"])
@jwt_required
def get_productos():
    productos = Producto.get_all()
    return jsonify(render_product_list(productos))


# Ruta para obtener un animal específico por su ID
@producto_bp.route("/producto/<int:id>", methods=["GET"])
@jwt_required
def get_producto(id):
    producto = Producto.get_by_id(id)
    if producto:
        return jsonify(render_product_detail(producto))
    return jsonify({"Error": "producto no encontrado"}),404


# Ruta para crear un nuevo animal
@producto_bp.route("/productos", methods=["POST"])
@jwt_required
@roles_required(roles="admin")
def create_productol():
    data = request.json
    name=data.get("name")
    description=data.get("description")
    price=data.get("price")
    stock=data.get("stock")
    # Validación simple de datos de entrada
    if not name or not description or price is None or stock is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo animal y guardarlo en la base de datos
    producto=Producto(name,description, price,stock)
    producto.save()

    return jsonify(render_product_detail(producto)), 201


# Ruta para actualizar un animal existente
@producto_bp.route("/productos/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles="admin")
def update_producto(id):
    producto = Producto.get_by_id(id)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.json
    name=data.get("name")
    description=data.get("description")
    price=data.get("price")
    stock=data.get("stock")
    
    producto.update(name,description,price,stock)

    return jsonify(render_product_detail(producto))


# Ruta para eliminar un animal existente
@producto_bp.route("/productos/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles="admin")
def delete_producto(id):
    producto=Producto.get_by_id(id)
    if not producto:
        return jsonify({"Error":"producto no encontrado"}), 404
    
    producto.delete()
    return "", 204

