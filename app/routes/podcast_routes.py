from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.podcast_controller import get_all_podcasts, get_podcast_by_id

podcast_routes = Blueprint('podcast_routes', __name__, url_prefix='/api/v1/podcast')


@podcast_routes.route('/', methods=['GET'])
def get_podcasts():
    return get_all_podcasts()

@podcast_routes.route('/id', methods=['GET'])
def get_podcast():
    return get_podcast_by_id()

"""@podcast_routes.route('/podcast-category', methods=['GET'])
def get_podcast_category():
    return get_categories()
"""
