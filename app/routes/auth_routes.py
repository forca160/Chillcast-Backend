from flask import request, Blueprint
from flask_jwt_extended import  jwt_required
from app.utils.required_roles import roles_requeridos
from app.controllers.auth_controller import register_user, login, logout, crear_usuario, invitar_usuario, invitar_al_chat, editar_usuario, obtener_usuarios
from app.utils.enums.roles_enum import Roles

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/api/v1/auth')

@auth_routes.route('/register-user', methods=['POST'])
def register_usuario():
    return register_user()

@auth_routes.route('/login', methods=['POST'])
def iniciar_sesion():
    return login()

@auth_routes.route('/logout', methods=['POST'])
@jwt_required()
def cerrar_sesion():
    return logout()

@auth_routes.route('/create-user', methods=['POST'])
@jwt_required()
@roles_requeridos(Roles.ADMINISTRADOR.value)
def create_user():
    return crear_usuario()

@auth_routes.route('/edit-user', methods=['PATCH'])
@jwt_required()
@roles_requeridos(Roles.ADMINISTRADOR.value)
def edit_user():
    return editar_usuario()

@auth_routes.route('/get-users', methods=['GET'])
@jwt_required()
@roles_requeridos(Roles.ADMINISTRADOR.value)
def get_users():
    return obtener_usuarios()

@auth_routes.route('/invite-user', methods=['GET'])
@jwt_required()
@roles_requeridos(Roles.ADMINISTRADOR.value)
def invite_user():
    return invitar_usuario()    

@auth_routes.route('/invite-to-chatbot', methods=['GET'])
@jwt_required()
@roles_requeridos(Roles.ADMINISTRADOR.value)
def invite_to_chatbo():
    return invitar_al_chat()  