from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.genero_service import genero_service

genero_routes = Blueprint('genero_routes', __name__, url_prefix='/api/v1/genero')


@genero_routes.route('/', methods=['GET'])
def get_generos():
    return genero_service().get_all_generos()

@genero_routes.route('/', methods=['POST'])
def crear_genero():
    print(request.json.get('genero'))
    return genero_service().create_gender(request.json.get('genero'))


