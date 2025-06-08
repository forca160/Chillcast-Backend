from app.database.models.genero import genero
from app.utils.logger import logger
from flask import jsonify
from bson import ObjectId
from dotenv import load_dotenv

class genero_service():

    logs = logger().get_logger()
    # Cargar variables de entorno desde el archivo .env
    load_dotenv()



    def get_all_generos(self):

        try:
            # Conectar al servidor MongoDB (por defecto, localhost:27017)
            podcastss = genero.objects()
            
                                   
            return jsonify(generos=podcastss.to_json())


        except Exception as e:
            # Manejo de otras excepciones
            print("Ocurrió un error:", e)
            # Otras acciones a realizar en caso de excepción
            
    def create_gender(self, gender):

        try:
            gender = genero(
                nombre_genero=gender
            )
            gender.save()
            
            return jsonify(genero=gender.to_json())
          
        except Exception as e:
            # Manejo de otras excepciones
            print("Ocurrió un error:", e)
            # Otras acciones a realizar en caso de excepción        
