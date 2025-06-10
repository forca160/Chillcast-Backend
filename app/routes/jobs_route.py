from flask import Blueprint, request
from app.services.jobs_service import jobs_service


jobs_routes = Blueprint('jobs_routes', __name__, url_prefix='/api/v1/jobs')


@jobs_routes.route('/', methods=['POST'])
def migrated_epi():
    return jobs_service().migrate_episodes()

@jobs_routes.route('/1', methods=['POST'])
def updated_epi():
    """
    Body JSON opcional:
      { "ids": ["60e5f8c2a2b4f23d5c9e12ab", "…"] }
    Si no envías 'ids', inicializa todos los podcasts.
    """
    return jobs_service().update_podcasts_with_genre_and_authors('update.json')

@jobs_routes.route('/2', methods=['POST'])
def updated_source():
    data = request.get_json()
    return jobs_service().update_source(data['source'])