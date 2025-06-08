from flask import Blueprint
from app.controllers.episodes_controller import get_episodes, obtener_episodios_segun_podcast


episode_routes = Blueprint("episode_routes", __name__, url_prefix="/api/v1/episode")


@episode_routes.route("/", methods=["GET"])
def get_podcast_episodes():
    return get_episodes()

@episode_routes.route("/episodes", methods=["GET"])
def get_episodes_by_podcast():
    return obtener_episodios_segun_podcast()