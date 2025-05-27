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
        return jsonify(podcasts=podcasts['documentos']), 200
    else:
        return jsonify({"error": "No se pudo realizar la búsqueda de podcasts"}), 400    

"""def agregar_animal():

    try:
        data = request.get_json()
        animal = animal_service().agregar_animal(
            animal_type=data['animal_type'],
            animal_quantity=data['animal_quantity'],
        )
        
        return jsonify({"message": 'se creo correctamente'}), 200
        
    except Exception as e:
        logs.warning('No se pudo guardar e animal por algún motivo' + e)
        return jsonify({"error": "No se pudo agregar el animal a la BBDD"}), 400"""