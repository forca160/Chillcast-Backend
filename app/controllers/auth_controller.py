from app.services.user_service import user_service
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
        request.json.get("username"),
        request.json.get("email"),
        request.json.get("password"),
        request.json.get("nombre"),
        request.json.get("apellido"),
        request.json.get("generos"),
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
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = user_service().verify_user(username, email, password)

    if user == "NO_EXISTE":
        return jsonify({"error": "El username o email no existe"}), 401
    elif not user:
        return jsonify({"error": "No se pudo obtener el usuario"}), 400
    else:
        return jsonify(user=user), 200


def delete():
    """ """
    username = request.json.get("username", None)
    email = request.json.get("email", None)

    user = user_service().delete_user(username, email)

    if user == "NO_EXISTE":
        return jsonify({"error": "El username o email no existen"}), 409
    elif not user:
        return jsonify({"error": "No se pudo borrar el usuario"}), 400
    else:
        return jsonify(user=user), 200


def get_user_favorites():
    username = request.args.get("username", None)
    email = request.args.get("email", None)

    user = user_service.get_favorites(username, email)

    if user == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif user == "NO_FAVORITOS":
        return jsonify({"error": "El usuario no tiene podcast favoritos"}), 404
    elif not user:
        return jsonify({"error": "No se pudo borrar el usuario"}), 400
    else:
        return jsonify(user=user), 200


def post_user_favorites():
    """ """
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    podcast = request.json.get("podcast", None)

    if not podcast:
        return jsonify({"error": "Campo podcast obligatorio"}), 400

    user = user_service.post_favorites(username, email, podcast)

    if user == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif user == "NO_FAVORITOS":
        return jsonify({"error": "El usuario no tiene podcast favoritos"}), 404
    elif not user:
        return jsonify({"error": "No se pudo borrar el usuario"}), 400
    else:
        return jsonify(user=user), 200
