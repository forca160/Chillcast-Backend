from app.services.user_service import user_service
from app.services.podcast_service import podcast_service
from flask import jsonify, request, current_app
from flask_bcrypt import Bcrypt
from app.utils.logger import logger
from dotenv import load_dotenv

bcrypt = Bcrypt()

load_dotenv()
log = logger().get_logger()


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
    if user == "YA_EXISTEN_AMBOS":
        return jsonify({"error": "El username y email ya existen"}), 409
    elif user == "YA_EXISTE_USERNAME":
        return jsonify({"error": "El username ya existe"}), 409
    elif user == "YA_EXISTE_EMAIL":
        return jsonify({"error": "El email ya existe"}), 409
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
    username = request.args.get("username", None)
    email = request.args.get("email", None)

    user = user_service().delete_user(username, email)

    if user == "NO_EXISTE":
        return jsonify({"error": "El username o email no existen"}), 409
    elif not user:
        return jsonify({"error": "No se pudo borrar el usuario"}), 400
    else:
        return jsonify(user=user), 200


def obtener_user():
    user = request.args.get("id_user")
    usuario = user_service().get_user_by_id(user)
    return jsonify(usuario=usuario)


def get_user_favorites():
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    favorites = user_service().get_favorites(username, email)

    if favorites == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif favorites == "NO_FAVORITOS":
        return jsonify({"error": "El usuario no tiene podcast favoritos"}), 404
    elif not favorites:
        return jsonify({"error": "No se pudieron obtener los favoritos"}), 400
    else:
        return jsonify(favorites=favorites), 200


def post_user_favorites():
    """ """
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    podcast = request.json.get("podcast", None)

    if not podcast:
        return jsonify({"error": "Campo podcast obligatorio"}), 400

    agrega = user_service().post_favorites(username, email, podcast)

    if agrega:
        favorites = user_service().get_favorites(username, email)
    else:
        favorites = None

    if favorites == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif favorites == "NO_FAVORITOS":
        return jsonify({"error": "El usuario no tiene podcast favoritos"}), 404
    elif not favorites:
        return jsonify({"error": "No se pudieron obtener los favoritos"}), 400
    else:
        return jsonify(favorites=favorites), 200


def delete_user_favorites():
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    podcast = request.json.get("podcast", None)

    if not podcast:
        return jsonify({"error": "Campo podcast obligatorio"}), 400

    borra = user_service().delete_favorites(username, email, podcast)

    if borra:
        favorites = user_service().get_favorites(username, email)
    else:
        favorites = None

    if favorites == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif favorites == "NO_FAVORITOS":
        return jsonify({"error": "El usuario no tiene podcast favoritos"}), 404
    elif not favorites:
        return jsonify({"error": "No se pudieron obtener los favoritos"}), 400
    else:
        return jsonify(favorites=favorites), 200


def edit_user():
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    data = {
        "generos_fav": request.json.get("generos", None),
        "nombre": request.json.get("nombre", None),
        "apellido": request.json.get("apellido", None),
    }
    user = user_service().edit_user(
        username, email, {k: v for k, v in data.items() if v}
    )

    if user == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    elif not user:
        return jsonify({"error": "No se pudo actualizar usuario"}), 400
    else:
        return jsonify(user=user), 200


def user_me():
    username = request.args.get("username", None)
    email = request.args.get("email", None)

    user = user_service().user_me(username, email)

    if user == "NO_EXISTE":
        return jsonify({"error": "El username o email no existen"}), 409
    elif not user:
        return jsonify({"error": "No se pudo borrar el usuario"}), 400
    else:
        return jsonify(user=user), 200


def post_user_poscasts():
    try:
        email = request.json.get("email")
        username = request.json.get("username")
        id_podcast = request.json.get("id_podcast")
    except Exception as e:
        print(e)
    try:

        # Actualizar el historial
        user = user_service().post_history(username, email, id_podcast)
        print(user)
        return jsonify(user=user), 200

    except ValueError as ve:
        # Usuario no encontrado
        return jsonify({"error": str(ve)}), 404

    except Exception as e:
        log.debug(f"post_history falló: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


def get_user_poscasts():
    email = request.args.get("email", None)
    username = request.args.get("username", None)

    history = user_service().get_history(username, email)

    return jsonify(history=history)


def obtener_recomendaciones():
    email = request.args.get("email", None)
    username = request.args.get("username", None)

    recomedaciones = user_service().obtener_recomendaciones(username, email)

    return jsonify(recomedaciones=recomedaciones)
