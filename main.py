from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.database.database_config import Config, init_db
from app.routes.podcast_routes import podcast_routes
from app.routes.auth_routes import auth_routes
from app.routes.jobs_route import jobs_routes
from app.routes.reviews_router import reviews_routes
from app.routes.genero_routes import genero_routes
from app.routes.episode_routes import episode_routes
from app.routes.listas_router import lista_routes
from datetime import timedelta
import os

load_dotenv()

jwt = JWTManager()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
TOKEN_EXPIRATION = os.getenv("JWT_ACCESS_TOKEN_EXPIRES")
# base_url = os.getenv("FRONT_BASE_URL")


def crear_app():

    # estos son los parametros de las rutas a las carpetas del Front
    app = Flask(
        __name__, static_folder="Frontend/dist/assets", template_folder="Frontend/dist"
    )
    app.config.from_object(Config)
    app.config["JWT_SECRET_KEY"] = SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(TOKEN_EXPIRATION))

    init_db()
    jwt.init_app(app)

    # CORS(app, resources={r"/*": {"origins": base_url}})

    cors = CORS(
        app,
        resources={
            r"/*": {
                "origins": "*",  # Permitir cualquier origen
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    app.register_blueprint(podcast_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(jobs_routes)
    app.register_blueprint(reviews_routes)
    app.register_blueprint(genero_routes)
    app.register_blueprint(lista_routes)
    app.register_blueprint(episode_routes)

    return app


app = crear_app()
if __name__ == "__main__":
    app.run(debug=True)
