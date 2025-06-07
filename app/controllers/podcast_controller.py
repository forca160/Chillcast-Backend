from flask import jsonify, request
from flask_bcrypt import Bcrypt
from app.utils.logger import logger
from app.services.podcast_service import podcast_service
from dotenv import load_dotenv


bcrypt = Bcrypt()

load_dotenv()

logs = logger().get_logger()

"""def get_categories():
    categories = podcast_service().get_categories()
    if categories != None:
        return jsonify(categories=categories['documentos']), 200
    else:
        return jsonify({"error": "No se pudo realizar la búsqueda de animales"}), 400"""
    
def get_all_podcasts():
    podcasts = podcast_service().get_all_podcasts()
    if podcasts != None:
        return jsonify(podcasts=podcasts.to_json()), 200
    else:
        return jsonify({"error": "No se pudo realizar la búsqueda de podcasts"}), 400    
    
def get_podcast_by_id():
    id_podcast = request.args.get('id')
    podcast = podcast_service().get_podcast_by_id(id_podcast)
    if podcast != None:
        return jsonify(podcasts=podcast.to_json()), 200
    else:
        return jsonify({"error": "No se pudo realizar la búsqueda de podcasts"}), 400      

