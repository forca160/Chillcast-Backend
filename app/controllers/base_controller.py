from flask import jsonify, send_from_directory
import os
from app.utils.logger import logger

logs = logger().get_logger()


def index():
    """
    Función para servir el archivo de índice.
    """
    return send_from_directory('Frontend/dist', 'index.html')


def serve_uploads(filename):
    """
    Función para servir archivos subidos por los usuarios.
    """
    uploads_path = os.path.join('app', 'uploads', 'flyers')
    return send_from_directory(uploads_path, filename)


def serve_static(filename):
    """
    Función para servir archivos estáticos.
    """
    return send_from_directory(os.path.join('Frontend/dist/assets'), filename)


def not_found(e):
    """
    Manejo de errores 404.
    """
    return send_from_directory('Frontend/dist', 'index.html')


def status():
    """
    Verifica el estado del backend.
    """
    return jsonify({"status": "ok", "message": "Blueprint is working!"})


def provincias():
    """
    Devuelve la lista de provincias de Argentina.
    """
    provincias_argentina = [
        "Buenos Aires",
        "Catamarca",
        "Chaco",
        "Chubut",
        "Córdoba",
        "Corrientes",
        "Entre Ríos",
        "Formosa",
        "Jujuy",
        "La Pampa",
        "La Rioja",
        "Mendoza",
        "Misiones",
        "Neuquén",
        "Río Negro",
        "Salta",
        "San Juan",
        "San Luis",
        "Santa Cruz",
        "Santa Fe",
        "Santiago del Estero",
        "Tierra del Fuego",
        "Tucumán"
    ]
    return jsonify(provincias_argentina), 200
