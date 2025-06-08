from app.database.models.users import Users
from app.utils.logger import logger
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime

bcrypt = Bcrypt()


class reviews_service:

    logs = logger().get_logger()

    load_dotenv()

    def json_document(self, documento):
        documento_list = list(documento)
        # Convierte ObjectId a string
        for doc in documento_list:
            doc["_id"] = str(doc["_id"])
        return documento_list

    def json_doc(self, documento):
        documento["_id"] = str(documento["_id"])
        return documento

    def create_user_review(self, username, email, review):
        # Verificar si el usuario ya está registrado
        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection_reviews = db["reviews"]
            collection_user = db["users"]

            data = collection_user.find_one(
                {"$or": [{"username": username}, {"email": email}]}
            )
            if not data:
                return "NO_EXISTE_USUARIO"

            review["user_id"] = str(data.get("_id"))

            post_id = collection_reviews.insert_one(review).inserted_id
            return True

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

    def get_user_reviews(self, username=None, email=None, id_review=None, podcast=None):
        # Verificar si el usuario ya está registrado
        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection_reviews = db["reviews"]
            collection_user = db["users"]

            user_id = None
            if username or email:
                data = collection_user.find_one(
                    {"$or": [{"username": username}, {"email": email}]}
                )
                if not data:
                    return "NO_EXISTE_USUARIO"
                user_id = str(data.get("_id"))

            documentos = list(
                collection_reviews.find(
                    {
                        "$or": [
                            {"user_id": user_id},
                            {"podcast_id": podcast},
                            {"_id": ObjectId(id_review)},
                        ]
                    },
                )
            )
            print(documentos)
            if not documentos:
                return "NO_EXISTEN_COMENTARIOS"

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
