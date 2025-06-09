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
    

    def buscar_podcasts(self, filtros):
        query = Q()


        # Filtro por título (campo simple)
        if 'title' in filtros and filtros['title']:
            query &= Q(title__icontains=filtros['title'])

        # Filtro por autor (lista de strings, requiere filtrado manual)
        if 'autores' in filtros and filtros['autores']:
            autor_buscado = filtros['autores'].lower()
            posibles = podcasts.objects(query & Q(autores__exists=True))
            resultados = []
            for p in posibles:
                if any(autor_buscado in autor.lower() for autor in p.autores):
                    resultados.append(p)
            return resultados # Salida anticipada si hay filtro por autor

        # Filtro por género (lista de strings, requiere filtrado manual)
        if 'genero' in filtros and filtros['genero']:
            genero_buscado = filtros['genero'].lower()
            posibles = podcasts.objects(query & Q(genero__exists=True))
            resultados = []
            for p in posibles:
                if any(genero_buscado in g.lower() for g in p.genero):
                    resultados.append(p)
            return resultados # Salida anticipada si hay filtro por género

        # Si solo hay filtro por título o ninguno
        return podcasts.objects(query)

