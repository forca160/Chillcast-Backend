from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.podcast_controller import get_categories, get_all_podcasts
"""from app.utils.required_roles import roles_requeridos
from app.utils.enums.roles_enum import Roles"""

podcast_routes = Blueprint('podcast_routes', __name__, url_prefix='/api/v1/podcast')

"""@podcast_routes.route('/', methods=['POST'])
def add_animal():
    return agregar_animal()"""

"""@podcast_routes.route('/animal-category', methods=['POST'])
@jwt_required()
@roles_requeridos(Roles.SUPER_ADMIN.value)
def add_animal_category():
    return agregar_categoria_animal()"""

@podcast_routes.route('/', methods=['GET'])
def get_podcasts():
    return get_all_podcasts()

@podcast_routes.route('/podcast-category', methods=['GET'])
def get_podcast_category():
    return get_categories()

