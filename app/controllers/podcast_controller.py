from flask import jsonify, request
from flask_bcrypt import Bcrypt
from app.utils.logger import logger
from app.services.podcast_service import podcast_service
from dotenv import load_dotenv
import json


bcrypt = Bcrypt()

load_dotenv()

logs = logger().get_logger()


def get_all_podcasts():
    podcasts = podcast_service().get_all_podcasts()
    if podcasts != None:
        # Serializamos los resultados manualmente
        resultado = []
        for p in podcasts:
            resultado.append(
                {
                    "GenreName": p.genero,
                    "author": p.autores,
                    "description": p.description,
                    "feed_url": p.feed_url,
                    "_id": str(p.id),
                    "image": p.image,
                    "language": p.language,
                    "source": p.source,
                    "title": p.title,
                    # Agregá más campos si querés
                }
            )
        return jsonify(podcasts=resultado), 200
    else:
        return jsonify({"error": "No se pudo realizar la búsqueda de podcasts"}), 400


def get_podcast_by_id():
    id_podcast = request.args.get("id")
    podcast = podcast_service().get_podcast_by_id(id_podcast)
    if podcast != None:
        # Serializamos los resultados manualmente
        resultado = []
        resultado.append(
            {
                "GenreName": podcast.genero,
                "author": podcast.autores,
                "description": podcast.description,
                "feed_url": podcast.feed_url,
                "_id": str(podcast.id),
                "image": podcast.image,
                "language": podcast.language,
                "source": podcast.source,
                "title": podcast.title,
                # Agregá más campos si querés
            }
        )
        return jsonify(podcasts=resultado), 200
    else:
        return jsonify({"error": "No se pudo realizar la búsqueda de podcasts"}), 400


def get_podcasts_by_genders():
    generos = request.args.getlist("generos")
    podcast = podcast_service().get_podcasts_by_gender(generos)
    if podcast != None:
        # Serializamos los resultados manualmente
        resultado = []
        for p in podcast:
            resultado.append(
                {
                    "GenreName": p.genero,
                    "author": p.autores,
                    "description": p.description,
                    "feed_url": p.feed_url,
                    "_id": str(p.id),
                    "image": p.image,
                    "language": p.language,
                    "source": p.source,
                    "title": p.title,
                    # Agregá más campos si querés
                }
            )
        return jsonify(podcasts=resultado), 200
    else:
        return jsonify({"error": "No se pudo realizar la búsqueda de podcasts"}), 400


def get_podcasts_by_author():

    author = request.args.get("autor")
    if not author:
        return jsonify({"error": "Falta el parámetro 'autor'"}), 400

    podcast_list = podcast_service().get_podcasts_by_author(author)

    if podcast_list:
        # Serializamos los resultados manualmente
        resultado = []
        for p in podcast_list:
            resultado.append(
                {
                    "GenreName": p.genero,
                    "author": p.autores,
                    "description": p.description,
                    "feed_url": p.feed_url,
                    "_id": str(p.id),
                    "image": p.image,
                    "language": p.language,
                    "source": p.source,
                    "title": p.title,
                    # Agregá más campos si querés
                }
            )
        return jsonify(podcasts=resultado), 200
    else:
        return jsonify({"error": "No se encontraron podcasts con ese autor"}), 404


def get_podcasts_by_filters():
    
    filtros = {}

    title = request.args.get('title')
    if title:
        filtros['title'] = title

    autores = request.args.get('autores')
    if autores:
        filtros['autores'] = autores

    genero = request.args.get('genero')
    if genero:
        filtros['genero'] = genero

    source = request.args.get('source')
    if source:
        filtros['source'] = source

    duracion = request.args.get('duracion')
    if duracion:
        try:
            filtros['duracion'] = int(duracion)
        except ValueError:
            pass  # Ignorar si no es un número válido

    resultado = podcast_service().buscar_podcasts(filtros)
    resultado = [podcast.to_json() for podcast in resultado]

    return jsonify(podcasts=resultado), 200
    