from flask import jsonify, request
from flask_bcrypt import Bcrypt
from app.utils.logger import logger
from dotenv import load_dotenv
from app.services.lista_service import lista_service

bcrypt = Bcrypt()

load_dotenv()


def get_user_lista():
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    lista = request.args.get("lista", None)

    listas = lista_service().get_user_lista(username, email, lista)

    if listas == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif listas == "NO_HAY_LISTAS":
        return jsonify({"error": "No se encontraron listas disponibles"}), 404
    elif not listas:
        return jsonify({"error": "No se pudieron obtener las listas"}), 400
    else:
        return jsonify(listas=listas), 200


def create_user_lista():
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    nombre_lista = request.json.get("nombre_lista")

    if not nombre_lista:
        return jsonify({"error": "Debe ingresar el nombre de la lista"}), 409

    listas = lista_service().create_user_lista(username, email, nombre_lista)

    if listas == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif not listas:
        return jsonify({"error": "No se pudieron obtener las listas"}), 400
    else:
        return jsonify(listas=listas), 200


def delete_user_lista():
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    lista = request.args.get("lista", None)

    listas = lista_service().delete_user_lista(username, email, lista)

    if listas == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif listas == "NO_EXISTE_LISTA":
        return jsonify({"error": "No se encontraron la lista solicitada"}), 404
    elif not listas:
        return jsonify({"error": "No se pudieron obtener las listas"}), 400
    else:
        return jsonify(listas=listas), 200


def update_user_lista(accion="UPDATE"):
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    lista = request.args.get("lista", None)
    podcast = request.args.get("podcast", None)

    if not podcast:
        return jsonify({"error": "Debe ingresar el podcast"}), 409

    if accion == "UPDATE":
        listas = lista_service().agregar_podcast(username, email, podcast, lista)
    elif accion == "DELETE":
        listas = lista_service().eliminar_podcast(username, email, podcast, lista)
    else:
        return jsonify({"error": "No se ingreso una accion valida"}), 400

    if listas == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif listas == "NO_EXISTE_LISTA":
        return jsonify({"error": "No se encontraron la lista solicitada"}), 404
    elif not listas:
        return jsonify({"error": "No se pudieron obtener las listas"}), 400
    else:
        return jsonify(listas=listas), 200
