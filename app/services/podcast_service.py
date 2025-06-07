from app.database.models.podcasts import podcasts
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
            podcastss = podcasts.objects()
            
                                   
            return podcastss


        except Exception as e:
            # Manejo de otras excepciones
            print("Ocurrió un error:", e)
            # Otras acciones a realizar en caso de excepción
            
    def get_podcast_by_id(self, documento_id):

        try:
            podcast = podcasts.objects(id=documento_id).first()
            
            return podcast
          
        except Exception as e:
            # Manejo de otras excepciones
            print("Ocurrió un error:", e)
            # Otras acciones a realizar en caso de excepción
          
        
    """def get_all_podcasts(self):
        documentos = podcasts.objects()  # Esto obtiene todos los documentos de la colección
        podcasts_serializados = [doc.to_json() for doc in documentos]
        return {'documentos': podcasts_serializados}
    """

    """def get_categories(self):
        documentos = podcasts.objects()  # Esto obtiene todos los documentos de la colección
        podcasts_serializados = [doc.to_json() for doc in documentos]
        return {'documentos': podcasts_serializados}"""    
    
    """def embeber_animales(self, animal_category, animal_subcategory, animal_breed, animal_quantity):
        try:
            animales = Animals(
                animal_category=animal_category,
                animal_subcategory=animal_subcategory,
                animal_breed=animal_breed,
                animal_quantity=animal_quantity
            )
            return animales
        
        except Exception as e:
            self.logs.warning(e)
            return False
        
    def agregar_categoria_animal(self, categoria):
        try:
            
            categoria = Animals_Categories(
                animal_category=categoria
            )
    
            if categoria.save():
                return categoria
        except Exception as e:
            self.logs.warning(e)
            return False        
        
    def agregar_subcategoria_animal(self, categoria_animal, subcategoria):
        try:
            
            subcategoria = Animals_Subcategories(
                animal_category=categoria_animal,
                animal_subcategory=subcategoria
            )
    
            if subcategoria.save():
                return subcategoria
        except Exception as e:
            self.logs.warning(e)
            return False                
        
    def get_category_by_name(self, category_name):

        categoria = Animals_Categories.objects(animal_category=category_name).first()
        if categoria != None:
            return categoria
        else:
            return False
        
    def get_subcategory_by_name(self, subcategory_name):

        subcategoria = Animals_Subcategories.objects(animal_subcategory=subcategory_name).first()
        if subcategoria != None:
            return subcategoria
        else:
            return False        
        
    def get_subcategorys(self):
        subcategoria = Animals_Subcategories.objects()
        return subcategoria
    """