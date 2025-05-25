from flask import Blueprint, request
from app.controllers.base_controller import (
    index,
    serve_uploads,
    serve_static,
    not_found,
    status
)

base_routes = Blueprint('base_routes', __name__, url_prefix='/api/v1')

# Ruta para servir el índice principal
base_routes.add_url_rule('/', 'index', index)

# Ruta para servir archivos subidos
@base_routes.route('/uploads/<filename>')
def uploads(filename):
    return serve_uploads(filename)

# Ruta para servir archivos estáticos
@base_routes.route('/<path:filename>')
def static_files(filename):
    return serve_static(filename)

# Manejo de errores 404
@base_routes.errorhandler(404)
def handle_not_found(e):
    return not_found(e)

# Ruta para verificar el estado del backend
@base_routes.route('/status', methods=['GET'])
def api_status():
    return status()

