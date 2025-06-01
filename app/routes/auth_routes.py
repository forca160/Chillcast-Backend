from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.auth_controller import register_user, login, delete

auth_routes = Blueprint("auth_routes", __name__, url_prefix="/api/v1/auth")


@auth_routes.route("/register-user", methods=["POST"])
def register_usuario():
    return register_user()


@auth_routes.route("/login", methods=["POST"])
def iniciar_sesion():
    return login()


@auth_routes.route("/logout", methods=["POST"])
def delete_user():
    return delete()
