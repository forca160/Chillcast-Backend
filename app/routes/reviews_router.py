from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.reviews_controller import post_user_review, get_user_review

reviews_routes = Blueprint("reviews_routes", __name__, url_prefix="/api/v1/reviews")


@reviews_routes.route("", methods=["POST"])
def post_review():
    return post_user_review()


@reviews_routes.route("", methods=["GET"])
def get_review():
    return get_user_review()
