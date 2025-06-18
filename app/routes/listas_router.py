from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.lista_controller import (
    get_user_lista,
    create_user_lista,
    delete_user_lista,
    update_user_lista,
)

lista_routes = Blueprint("lista_routes", __name__, url_prefix="/api/v1/listas")


@lista_routes.route("", methods=["GET"])
def get_listas():
    return get_user_lista()


@lista_routes.route("", methods=["POST"])
def crear_lista():
    return create_user_lista()


@lista_routes.route("", methods=["DELETE"])
def delete_lista():
    return delete_user_lista()


@lista_routes.route("/podcast", methods=["PUT"])
def actualiza_lista():
    return update_user_lista("UPDATE")


@lista_routes.route("/podcast", methods=["DELETE"])
def borra_podcast_lista():
    return update_user_lista("DELETE")
