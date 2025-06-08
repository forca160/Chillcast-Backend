from app.services.reviews_service import reviews_service
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from app.utils.logger import logger
from dotenv import load_dotenv

bcrypt = Bcrypt()

load_dotenv()


def post_user_review():
    """
    Se cargan las reseñas del usuario, despues se devuelven las totalidad de las reseñas
    """
    username = request.args.get("username", None)
    email = request.args.get("email", None)

    comment = request.json.get("comment", None)
    qualification = request.json.get("qualification", None)
    podcast = request.json.get("podcast", None)

    if not qualification:
        return jsonify({"error": "Campo qualification obligatorio"}), 400
    if not podcast:
        return jsonify({"error": "Campo podcast obligatorio"}), 400

    if not reviews_service().create_user_review(
        username,
        email,
        {"comment": comment, "qualification": qualification, "podcast_id": podcast},
    ):
        return jsonify({"error": "No se pudieron obtener los favoritos"}), 400

    reviews = reviews_service().get_user_reviews(podcast=podcast)

    if reviews == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    if not reviews:
        return jsonify({"error": "No se pudieron obtener los favoritos"}), 400
    else:
        return jsonify(reviews=reviews), 200


def get_user_review():
    """"""
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    review = request.args.get("review", None)
    podcast = request.args.get("podcast", None)

    reviews = reviews_service().get_user_reviews(username, email, review, podcast)

    if reviews == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    if reviews == "NO_EXISTEN_COMENTARIOS":
        return (
            jsonify({"error": "No existen comentarios para los parametros ingresados"}),
            404,
        )
    if not reviews:
        return jsonify({"error": "No se pudieron obtener los favoritos"}), 400
    else:
        return jsonify(reviews=reviews), 200


def delete_user_review():
    username = request.args.get("username", None)
    email = request.args.get("email", None)
    review = request.args.get("review", None)
    podcast = request.args.get("podcast", None)

    if not review:
        return jsonify({"error": "Campo review obligatorio"}), 400

    if not reviews_service().delete_user_reviews(review):
        return jsonify({"error": "No se pudieron obtener los favoritos"}), 400

    reviews = reviews_service().get_user_reviews(podcast=podcast)

    if reviews == "NO_EXISTE_USUARIO":
        return jsonify({"error": "El username o email no existen"}), 409
    if reviews == "NO_EXISTEN_COMENTARIOS":
        return (
            jsonify({"error": "No existen comentarios para los parametros ingresados"}),
            404,
        )
    if not reviews:
        return jsonify({"error": "No se pudieron obtener los favoritos"}), 400
    else:
        return jsonify(reviews=reviews), 200
