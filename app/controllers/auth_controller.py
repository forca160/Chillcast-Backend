from services.user_service import user_service
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from app.utils.logger import logger
from dotenv import load_dotenv

bcrypt = Bcrypt()

load_dotenv()


def register_user():
    """
    Se inserta el usuario en la base de datos
    """
    user = user_service().create_user(
        request.args.get("username"),
        request.args.get("email"),
        request.args.get("password"),
        request.args.get("nombre"),
        request.args.get("apellido"),
        request.args.get("generos"),
    )

    if user == "YA_EXISTE":
        return jsonify({"error": "El username o email ya existen"}), 409
    elif not user:
        return jsonify({"error": "No se pudo insertar el usuario"}), 400
    else:
        return jsonify(user=user), 200


def login():
    """
    Logeo del usuario
    """
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    password = request.args.get("password", None)

    user = user_service().create_user(username, email, password)

    if user == "NO_EXISTE":
        return jsonify({"error": "El username o email no existe"}), 401
    elif not user:
        return jsonify({"error": "No se pudo obtener el usuario"}), 400
    else:
        return jsonify(user=user), 200


def delete():
    """ """
    username = request.args.get("username", None)
    email = request.args.get("email", None)

    user = user_service().delete_user(username, email)

    if user == "NO_EXISTE":
        return jsonify({"error": "El username o email no existen"}), 409
    elif not user:
        return jsonify({"error": "No se pudo borrar el usuario"}), 400
    else:
        return jsonify(user=user), 200
