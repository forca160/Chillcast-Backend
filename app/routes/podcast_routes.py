from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.controllers.podcast_controller import get_all_podcasts, get_podcast_by_id, get_podcasts_by_genders, get_podcasts_by_author

podcast_routes = Blueprint('podcast_routes', __name__, url_prefix='/api/v1/podcast')


@podcast_routes.route('/', methods=['GET'])
def get_podcasts():
    return get_all_podcasts()

@podcast_routes.route('/id', methods=['GET'])
def get_podcast():
    return get_podcast_by_id()

@podcast_routes.route('/genders', methods=['GET'])
def get_podcasts_by_id():
    return get_podcasts_by_genders()

@podcast_routes.route('/author', methods=['GET'])
def obtener_podcasts_segun_autor():
    return get_podcasts_by_author()

