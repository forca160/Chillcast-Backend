from app.services.episode_service import episode_service
from app.services.podcast_service import podcast_service
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from app.utils.logger import logger
from dotenv import load_dotenv

bcrypt = Bcrypt()

load_dotenv()
logs = logger().get_logger()


def get_episodes():
    """"""
    episode = request.args.get("episode", None)
    podcast = request.args.get("podcast", None)

    episodes = episode_service().episodes(podcast, episode)

    if episodes == "PODCAST_INEXISTENTE":
        return jsonify({"error": "Podcast ingresado no existe"}), 404
    elif episodes == "FALTAN_CAMPOS":
        return jsonify({"error": "No se ingresaron campos"}), 400
    elif not episodes:
        return jsonify({"error": "No se pudieron obtener episodios"}), 400
    else:
        return jsonify(episodes=episodes), 200

def obtener_episodios_segun_podcast():
    id_podcast = request.args.get('id_podcast')
    episodes = episode_service().get_episodes_by_podcast(id_podcast)
    

    return jsonify(episodes=episodes)
