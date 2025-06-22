from app.database.models.users import Users
from app.utils.logger import logger
from flask_bcrypt import Bcrypt
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ConnectionFailure
import os
from bson.objectid import ObjectId, InvalidId
from dotenv import load_dotenv
from datetime import datetime
from app.database.database_config import db

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
            return False

    def register_user(self, username, email, password, nombre, apellido, generos_fav):
        # Verificar si el usuario ya está registrado
        try:
            user = Users(
                username=username,
                email= email,
                password= password,
                nombre= nombre,
                apellido= apellido,
                generos_fav= generos_fav,
                activo= True,
                fecha_alta= datetime.today(),
            )
            user.save()
            """if data_username and data_email:
                return "YA_EXISTEN_AMBOS"
            elif data_username:
                return "YA_EXISTE_USERNAME"
            elif data_email:
                return "YA_EXISTE_EMAIL"""

            
            return user

        except ConnectionFailure:
            # Manejo de la excepción ConnectionFailure
            print("Error de conexión con la base de datos MongoDB.")
            # Otras acciones a realizar en caso de excepción

        except Exception as e:
            # Manejo de otras excepciones
            print("Ocurrió un error:", e)
            # Otras acciones a realizar en caso de excepción
            return False
        
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

    def get_user_by_id(self, id_user: str) -> dict | None:
        """
        Recupera un usuario por su ID.
        
        Parámetros:
            id_user (str): El identificador del usuario. Puede ser un ObjectId (hex string)
                            o un valor de campo 'id_user' si así lo tienes modelado.
                            
        Retorna:
            dict | None: Documento del usuario si lo encuentra, o None si no existe.
        """
        client = MongoClient(os.getenv("MONGODB_HOST"))

        # Acceder a la base de datos
        db = client[os.getenv("MONGODB_DB")]

        # Acceder a la colección usuarios
        collection_users = db["users"]
        try:
            query = {"_id": ObjectId(id_user)}
        except Exception:
            query = {"id_user": id_user}
        doc = collection_users.find_one(query)
        if doc is None:
            return None
        
        return self.json_doc(doc)
    
    def get_user_by_email(self, email: str):
        
        user = Users.objects(email=email).first()

        if user is None:
            return None
        
        return user  

    def get_user_by_username_email(self, username: str, email: str):
        """
        Conecta a MongoDB y devuelve el documento de usuario que coincida
        tanto en 'username' como en 'email'.

        :param mongo_uri: URI de conexión a MongoDB (p.ej. "mongodb://localhost:27017")
        :param db_name: Nombre de la base de datos
        :param username: Username a buscar
        :param email: Email a buscar
        :return: Diccionario con el usuario, o None si no existe
        """
        client = MongoClient(os.getenv("MONGODB_HOST"))
        db = client[os.getenv("MONGODB_DB")]
        collection = db['users']

        query = {
            'username': username,
            'email': email
        }
        user = collection.find_one(query)
        client.close()
        return user
    
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

    def post_history(self, username, email, id_podcast):
        
        client = MongoClient(os.getenv("MONGODB_HOST"))
        db = client[os.getenv("MONGODB_DB")]
        collection = db['users']
        pods_col  = db['podcasts']


        # 2) Buscar el podcast por su ID
        try:
            oid = ObjectId(id_podcast)
        except InvalidId:
            client.close()
            raise ValueError(f"ID de podcast inválido: {id_podcast}")
        
        podcast_doc = pods_col.find_one({'_id': oid})
        if not podcast_doc:
            client.close()
            raise ValueError(f"Podcast con id '{id_podcast}' no existe.")
        
        # 3) Actualizar el historial del usuario (embed del doc completo)
        query = {'username': username, 'email': email}
        updated_user = collection.find_one_and_update(
            query,
            {'$push': {'history': podcast_doc}},
            return_document=ReturnDocument.AFTER
        )
        client.close()
        
        if not updated_user:
            raise ValueError(f"Usuario '{username}' con email '{email}' no existe.")
        
        return updated_user
    
    def get_history(self, username: str, email: str) -> list:
        """
        Devuelve la lista 'history' del usuario identificado por username y email.
        Lanza ValueError si no existe el usuario.
        """
        # Conexión
        client = MongoClient(os.getenv("MONGODB_HOST"))
        db     = client[os.getenv("MONGODB_DB")]
        users  = db['users']

        # Buscar solo el campo history
        doc = users.find_one(
            {'username': username, 'email': email},
            {'history': 1, '_id': 0}
        )
        client.close()

        if not doc:
            raise ValueError(f"Usuario '{username}' con email '{email}' no existe.")

        history = doc.get('history', [])

        # Función recursiva para convertir ObjectId a string
        def _stringify(obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            elif isinstance(obj, dict):
                return {k: _stringify(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_stringify(v) for v in obj]
            else:
                return obj

        return _stringify(history)    
    
    def obtener_recomendaciones(self, username, email):
        """
        Devuelve un dict con:
          - 'generos_fav': lista de hasta 5 podcasts aleatorios que compartan
                           al menos un género de user.generos_fav
          - 'segun_escuchados': lista de hasta 5 podcasts que compartan género
                                o autor con los últimos 5 escuchados
        Lanza ValueError si no existe el usuario.
        """
        client = MongoClient(os.getenv("MONGODB_HOST"))
        try:
            db        = client[os.getenv("MONGODB_DB")]
            users_col = db['users']
            pods_col  = db['podcasts']

            # 1) Traer sólo generos_fav y history del user
            user = users_col.find_one(
                {'username': username, 'email': email},
                {'generos_fav': 1, 'history': 1}
            )
            if not user:
                raise ValueError(f"Usuario '{username}' con email '{email}' no existe.")

            fav_genres = user.get('generos_fav', [])
            history    = user.get('history', [])

            # Función recursiva para convertir ObjectId a str
            def _stringify(obj):
                if isinstance(obj, ObjectId):
                    return str(obj)
                elif isinstance(obj, dict):
                    return {k: _stringify(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [_stringify(v) for v in obj]
                else:
                    return obj

            # 2) Recomendados por géneros favoritos
            generos_fav_list = []
            if fav_genres:
                pipeline = [
                    {'$match': {'genero': {'$in': fav_genres}}},
                    {'$sample': {'size': 5}}
                ]
                docs = pods_col.aggregate(pipeline)
                generos_fav_list = [_stringify(doc) for doc in docs]

            # 3) Recomendados según escuchados
            segun_escuchados_list = []
            if history:
                ultimos = history[-5:]
                genres_hist  = set()
                authors_hist = set()
                for p in ultimos:
                    # p es un dict ya embebido; extraemos géneros y autor
                    for g in (p.get('genero') or []):
                        genres_hist.add(g)
                    a = p.get('author') or p.get('autores')
                    if a:
                        authors_hist.add(a)

                filters = []
                if genres_hist:
                    filters.append({'genero': {'$in': list(genres_hist)}})
                if authors_hist:
                    filters.append({'author': {'$in': list(authors_hist)}})

                if filters:
                    cursor = pods_col.find({'$or': filters}).limit(10)
                    segun_escuchados_list = [_stringify(doc) for doc in cursor]

            return {
                'generos_fav': generos_fav_list,
                'segun_escuchados': segun_escuchados_list
            }

        finally:
            client.close()