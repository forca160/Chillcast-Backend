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


class user_service:

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

    def create_user(self, username, email, password, nombre, apellido, generos_fav):
        # Verificar si el usuario ya está registrado
        try:
            user_dict = {
                "username": username,
                "email": email,
                "password": password,
                "nombre": nombre,
                "apellido": apellido,
                "generos_fav": generos_fav,
                "activo": True,
                "fecha_alta": datetime.today(),
            }
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection = db["users"]

            data_username = collection.find_one({"username": username})
            data_email = collection.find_one({"email": email})

            if data_username and data_email:
                return "YA_EXISTEN_AMBOS"
            elif data_username:
                return "YA_EXISTE_USERNAME"
            elif data_email:
                return "YA_EXISTE_EMAIL"

            post_id = collection.insert_one(user_dict).inserted_id
            documentos = collection.find(
                {"_id": ObjectId(post_id)},
                {"password": 0, "favorites": 0},
            )
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

    def edit_user(self, username, email, data):
        # Verificar si el usuario ya está registrado
        try:
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection = db["users"]

            documentos_usuarios = collection.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                    "activo": True,
                },
                {"password": 0},
            )

            if not documentos_usuarios:
                return "NO_EXISTE_USUARIO"
            collection.update_one(
                {"_id": documentos_usuarios.get("_id")}, {"$set": data}
            )
            documentos = list(
                collection.find(
                    {
                        "_id": documentos_usuarios.get("_id"),
                    },
                    {"password": 0},
                )
            )
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

    def user_me(self, username, email):
        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection = db["users"]

            documentos = collection.find(
                {
                    "$or": [{"username": username}, {"email": email}],
                },
                {"password": 0, "favorites": 0},
            )

            if not documentos:
                return "NO_EXISTE"

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

    def verify_user(self, username, email, password):
        try:
            user_dict = {"username": username, "email": email, "password": password}
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection = db["users"]

            documentos = collection.find(
                {
                    "$or": [{"username": username}, {"email": email}],
                    "password": password,
                    "activo": True,
                },
                {"password": 0, "favorites": 0},
            )

            if not documentos:
                return "NO_EXISTE"

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

    def delete_user(self, username, email):
        try:
            user_dict = {"username": username, "email": email}
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection = db["users"]

            documentos = collection.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                    "activo": True,
                },
                {"password": 0},
            )

            if not documentos:
                return "NO_EXISTE"

            collection.update_one(
                {"_id": ObjectId(documentos.get("_id"))}, {"$set": {"activo": False}}
            )

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

    def get_favorites(self, username, email):
        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección usuarios
            collection_users = db["users"]

            # Accede a la collecion de podcast
            collection_podcast = db["podcasts"]

            documentos_usuarios = collection_users.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                    "activo": True,
                },
                {"password": 0},
            )

            if not documentos_usuarios:
                return "NO_EXISTE_USUARIO"

            if not documentos_usuarios.get("favorites", None):
                return "NO_FAVORITOS"

            favorites = [
                ObjectId(fav) for fav in documentos_usuarios.get("favorites", [])
            ]

            documentos_podcast = list(
                collection_podcast.find({"_id": {"$in": favorites}})
            )

            if not documentos_podcast:
                return "NO_FAVORITOS"

            for doc in documentos_podcast:
                doc["episodes"] = [str(ep) for ep in doc.get("episodes")]

            print(documentos_podcast)

            return self.json_document(documentos_podcast)

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

    def post_favorites(self, username, email, podcast):
        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección usuarios
            collection_users = db["users"]

            documentos_usuarios = collection_users.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                    "activo": True,
                },
                {"password": 0},
            )

            if not documentos_usuarios:
                return "NO_EXISTE_USUARIO"

            documentos_usuarios = collection_users.update_one(
                {"_id": ObjectId(documentos_usuarios.get("_id"))},
                {"$addToSet": {"favorites": podcast}},
            )

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

    def delete_favorites(self, username, email, podcast):
        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección usuarios
            collection_users = db["users"]

            documentos_usuarios = collection_users.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                    "activo": True,
                },
                {"password": 0},
            )

            if not documentos_usuarios:
                return "NO_EXISTE_USUARIO"

            documentos_usuarios = collection_users.update_one(
                {"_id": ObjectId(documentos_usuarios.get("_id"))},
                {"$pull": {"favorites": podcast}},
            )

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
