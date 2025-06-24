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


class lista_service:

    def json_document(self, documento):
        documento_list = list(documento)
        # Convierte ObjectId a string
        for doc in documento_list:
            doc["_id"] = str(doc["_id"])
        return documento_list

    def json_doc(self, documento):
        documento["_id"] = str(documento["_id"])
        return documento

    def get_user_lista(self, username, email, lista=None):
        # Verificar si el usuario ya está registrado
        try:

            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection_listas = db["listas"]
            collection_users = db["users"]

            documentos_user = collection_users.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                },
                {"password": 0, "favorites": 0},
            )

            if not documentos_user:
                return "NO_EXISTE_USUARIO"

            filtro = (
                {"user": str(documentos_user.get("_id"))}
                if not lista
                else {
                    "user": str(documentos_user.get("_id")),
                    "_id": ObjectId(lista),
                }
            )

            documentos = list(collection_listas.find(filtro))

            if not documentos:
                return "NO_HAY_LISTAS"

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

    def create_user_lista(self, username, email, nombre_lista):
        # Verificar si el usuario ya está registrado
        try:

            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection_listas = db["listas"]
            collection_users = db["users"]

            documentos_user = collection_users.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                },
                {"password": 0, "favorites": 0},
            )

            if not documentos_user:
                return "NO_EXISTE_USUARIO"

            data = {
                "user": str(documentos_user.get("_id")),
                "nombre": nombre_lista,
                "podcast": [],
            }

            collection_listas.insert_one(data)

            return self.get_user_lista(username, email)
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

    def delete_user_lista(self, username, email, lista):
        # Verificar si el usuario ya está registrado
        try:

            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection_listas = db["listas"]
            collection_users = db["users"]

            documentos_user = collection_users.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                },
                {"password": 0, "favorites": 0},
            )

            if not documentos_user:
                return "NO_EXISTE_USUARIO"

            if not collection_listas.find_one({"_id": ObjectId(lista)}):
                return "NO_EXISTE_LISTA"

            collection_listas.delete_one({"_id": ObjectId(lista)})

            return self.get_user_lista(username, email)
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

    def agregar_podcast(self, username, email, podcast, lista):
        # Verificar si el usuario ya está registrado
        try:

            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection_listas = db["listas"]
            collection_users = db["users"]

            documentos_user = collection_users.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                },
                {"password": 0, "favorites": 0},
            )

            if not documentos_user:
                return "NO_EXISTE_USUARIO"

            if not collection_listas.find_one({"_id": ObjectId(lista)}):
                return "NO_EXISTE_LISTA"

            collection_listas.update_one(
                {"_id": ObjectId(lista)},
                {"$addToSet": {"podcast": podcast}},
            )

            return self.get_user_lista(username, email)
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

    def eliminar_podcast(self, username, email, podcast, lista):
        # Verificar si el usuario ya está registrado
        try:

            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv("MONGODB_HOST"))

            # Acceder a la base de datos
            db = client[os.getenv("MONGODB_DB")]

            # Acceder a la colección
            collection_listas = db["listas"]
            collection_users = db["users"]

            documentos_user = collection_users.find_one(
                {
                    "$or": [{"username": username}, {"email": email}],
                },
                {"password": 0, "favorites": 0},
            )

            if not documentos_user:
                return "NO_EXISTE_USUARIO"

            if not collection_listas.find_one({"_id": ObjectId(lista)}):
                return "NO_EXISTE_LISTA"

            collection_listas.update_one(
                {"_id": ObjectId(lista)},
                {"$pull": {"podcast": podcast}},
            )

            return self.get_user_lista(username, email)
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
