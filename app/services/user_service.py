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

            data = collection.find_one(
                {"$or": [{"username": username}, {"email": email}]}
            )
            print(data)
            if data:
                return "YA_EXISTE"

            post_id = collection.insert_one(user_dict).inserted_id
            documentos = collection.find(
                {"_id": ObjectId(post_id)},
                {"password": 0},
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

    def edit_user(self, user, data):
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.save()
        return user

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
                {"password": 0},
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
                    "$or": [{"username": username, "email": email}],
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

    # def check_duplicate_usernames(self, usernames):
    #     try:
    #         # Buscar usernames duplicados en la base de datos
    #         existing_users = Users.objects(username__in=usernames).only("username")
    #         duplicates = [user.username for user in existing_users]
    #         return duplicates
    #     except Exception as e:
    #         self.logs.error(f"Error al verificar usuarios duplicados: {e}")
    #         raise RuntimeError("Error al verificar usuarios duplicados") from e

    # def get_user_by_email(self, email):
    #     return Users.objects(email=email).first()

    # def get_user_by_id(self, id_user):
    #     return Users.objects(id=id_user).first()

    # def get_users_by_enterprise(self, enterprise):
    #     return Users.objects(enterprise=enterprise)

    # def add_field_to_user(self, field, user):
    #     try:
    #         user.fields.append(field)
    #         user.save()
    #         print(user.email)
    #         self.logs.info("Se guardó el campo en el usuario")
    #         return True
    #     except Exception as e:
    #         self.logs.warning(e)
    #         return False
