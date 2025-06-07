#from app.database.models.podcasts import podcasts
from app.utils.logger import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
import os
from dotenv import load_dotenv

class podcast_service():

    logs = logger().get_logger()
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()


    def json_document(self, documento):
        documento_list = list(documento)
        # Convierte ObjectId a string
        for doc in documento_list:
            doc['_id'] = str(doc['_id'])
            doc.pop('episodes', None)
        return documento_list
    
    def json_doc(self, documento):
        documento['_id'] = str(documento['_id'])
        documento.pop('episodes')
        return documento

        
    def get_all_podcasts(self):

        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv('MONGODB_HOST'))
            
            # Acceder a la base de datos
            db = client[os.getenv('MONGODB_DB')]
            
            # Acceder a la colección
            collection = db['podcasts']
            
            # Obtener todos los documentos de la colección
            documentos = list(collection.find())
            
                        
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
            if 'client' in locals():
                client.close()

    def get_podcast_by_id(self, documento_id):

        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            client = MongoClient(os.getenv('MONGODB_HOST'))
            
            # Acceder a la base de datos
            db = client[os.getenv('MONGODB_DB')]
            
            # Acceder a la colección
            collection = db['podcasts']
            # Convertir el ID de cadena a ObjectId
            obj_id = ObjectId(documento_id)
            # Buscar el documento por su ID
            documento = collection.find_one({"_id": obj_id})
            print(documento)

            return self.json_doc(documento) if documento else None            

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
            if 'client' in locals():
                client.close()                
        