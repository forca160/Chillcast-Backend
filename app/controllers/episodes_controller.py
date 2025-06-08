from app.services.episode_service import episode_service
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from app.utils.logger import logger
from dotenv import load_dotenv

bcrypt = Bcrypt()

load_dotenv()


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
