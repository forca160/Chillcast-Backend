from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.auth_controller import (
    register_user,
    login,
    delete,
    get_user_favorites,
    post_user_favorites,
    delete_user_favorites,
    edit_user,
    user_me,
    obtener_user,
    post_user_poscasts,
    get_user_poscasts,
    obtener_recomendaciones
)

auth_routes = Blueprint("auth_routes", __name__, url_prefix="/api/v1/auth")


@auth_routes.route("/register-user", methods=["POST"])
def register_usuario():
    return register_user()


@auth_routes.route("/login", methods=["POST"])
def iniciar_sesion():
    return login()


@auth_routes.route("/delete", methods=["DELETE"])
def delete_user():
    return delete()


@auth_routes.route("/favorites", methods=["GET"])
def get_favorites():
    return get_user_favorites()


@auth_routes.route("/favorites", methods=["POST"])
def post_favorites():
    return post_user_favorites()


@auth_routes.route("/favorites", methods=["DELETE"])
def delete_favorites():
    return delete_user_favorites()

@auth_routes.route("/history", methods=["POST"])
def post_podcast():
    return post_user_poscasts()

@auth_routes.route("/history", methods=["GET"])
def get_podcast():
    return get_user_poscasts()

@auth_routes.route("/edit-user", methods=["PUT"])
def put_user():
    return edit_user()


@auth_routes.route("/user-me", methods=["GET"])
def get_user_me():
    return user_me()

@auth_routes.route("/get-user", methods=["GET"])
def get_user():
    return obtener_user()

@auth_routes.route("/get-recomendations", methods=["GET"])
def get_recomendations():
    return obtener_recomendaciones()