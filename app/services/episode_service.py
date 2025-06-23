from app.database.models.podcasts import podcasts
from app.utils.logger import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
import os
from dotenv import load_dotenv


class episode_service:

    logs = logger().get_logger()
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()

    def json_document(self, documento):
        documento_list = list(documento)
        # Convierte ObjectId a string
        for doc in documento_list:
            doc["_id"] = str(doc["_id"])
            doc.pop("episodes", None)
        return documento_list

    def json_doc(self, documento):
        documento["_id"] = str(documento["_id"])
        documento.pop("episodes")
        return documento

    def episodes(self, podcast, episode):

        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection_podcast = db["podcasts"]
            collection_episode = db["episodes"]

            if episode:
                documentos = list(
                    collection_episode.find(
                        {"_id": ObjectId(episode)},
                        {"podcast_id": 0, "provider_episode_id": 0},
                    )
                )
            elif podcast:
                # Obtener todos los documentos de la colección
                documentos_podcast = collection_podcast.find_one(
                    {"_id": ObjectId(podcast)}
                )

                if not documentos_podcast:
                    return "PODCAST_INEXISTENTE"

                documentos = list(
                    collection_episode.find(
                        {"_id": {"$in": documentos_podcast.get("episodes")}},
                        {"podcast_id": 0, "provider_episode_id": 0},
                    )
                )
            else:
                return "FALTAN_CAMPOS"

            return self.json_document(documentos)

        except ConnectionFailure:
            # Manejo de la excepción ConnectionFailure
            print("Error de conexión con la base de datos MongoDB.")
            # Otras acciones a realizar en caso de excepción

        except Exception as e:
            # Manejo de otras excepciones
            print("Ocurrió un error:", e)
            # Otras acciones a realizar en caso de excepción

        finally:
            # Acciones a realizar después del bloque try-except, como cerrar conexiones
            if "client" in locals():
                client.close()

    def get_episodes_by_podcast(self, podcast_id):

        podcast = podcasts.objects(id=podcast_id).first()

        episodes_data = []
        for ep in podcast.episodes:
            episodes_data.append(
                {
                    "title": ep.title,
                    "description": ep.description,
                    # agregá más campos según tu modelo
                }
            )
        return episodes_data
