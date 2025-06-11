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
    podcasts = [podcast.to_json() for podcast in podcasts]
    return jsonify(podcasts=podcasts), 200
    

def get_podcast_by_id():
    id_podcast = request.args.get("id")
    podcast = podcast_service().get_podcast_by_id(id_podcast)
    if podcast != None:
        # Serializamos los resultados manualmente

        return jsonify(podcasts=podcast.to_json()), 200
    else:
        return jsonify({"error": "No se pudo realizar la búsqueda de podcasts"}), 400


def get_podcasts_by_genders():
    generos = request.args.getlist("generos")
    podcasts = podcast_service().get_podcasts_by_gender(generos)
    podcasts = [podcast.to_json() for podcast in podcasts]
    return jsonify(podcasts=podcasts), 200
        

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

    # Soporte para múltiples géneros (AND)
    generos = request.args.getlist('genero')
    if len(generos) == 1 and ',' in generos[0]:
        generos = [g.strip() for g in generos[0].split(',') if g.strip()]
    if generos:
        filtros['generos'] = generos

    source = request.args.get('source')
    if source:
        filtros['source'] = source

    # ------ NUEVO: RANGO de duración ------
    dur_min = request.args.get('duracion_min')
    dur_max = request.args.get('duracion_max')
    try:
        if dur_min is not None:
            filtros['duracion_min'] = float(dur_min)
        if dur_max is not None:
            filtros['duracion_max'] = float(dur_max)
    except ValueError:
        # Si no son números válidos, ignoramos el filtro
        pass

    resultado = podcast_service().buscar_podcasts(filtros)
    resultado = [pod.to_json() for pod in resultado]
    return jsonify(podcasts=resultado), 200
