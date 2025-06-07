from flask import Blueprint
from app.controllers.podcast_controller import get_all_podcasts, get_podcast_by_id


episode_routes = Blueprint('episode_routes', __name__, url_prefix='/api/v1/episode')


@episode_routes.route('/', methods=['GET'])
def get_episodes():
    return get_all_episodes()

@episode_routes.route('/id', methods=['GET'])
def get_podcast():
    return get_podcast_by_id()


