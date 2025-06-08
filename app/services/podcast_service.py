from app.database.models.podcasts import podcasts
from app.utils.logger import logger
from dotenv import load_dotenv
from mongoengine.queryset.visitor import Q

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
          
    def get_podcasts_by_gender(self, genders):    
        podcastss = podcasts.objects(genero__all=genders)

        return podcastss
    
    def get_podcasts_by_author(self, author_name):    

        posibles = podcasts.objects(autores__exists=True)

        filtrados = []
        for p in posibles:
            if any(author_name.lower() in autor.lower() for autor in p.autores):
                filtrados.append(p)

        return filtrados
