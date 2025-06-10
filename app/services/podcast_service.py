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

        if 'title' in filtros:
            query &= Q(title__icontains=filtros['title'])

        if 'source' in filtros:
            query &= Q(source__icontains=filtros['source'])

        posibles = podcasts.objects(query)

        # Filtro por autor
        if 'autores' in filtros:
            autor_buscado = filtros['autores'].lower()
            posibles = [p for p in posibles if any(autor_buscado in autor.lower() for autor in p.autores)]

        # Filtro por género
        if 'genero' in filtros:
            genero_buscado = filtros['genero'].lower()
            posibles = [p for p in posibles if any(genero_buscado in g.lower() for g in p.genero)]

        # Filtro por duración promedio de los primeros 3 episodios
        if 'duracion' in filtros:
            duracion_max_min = filtros['duracion']
            filtrados = []
            for p in posibles:
                episodios = p.episodes[:3]  # primeros 3 episodios
                if not episodios:
                    continue
                duraciones = [ep.duration_ms for ep in episodios if hasattr(ep, 'duration_ms') and ep.duration_ms]
                if not duraciones:
                    continue
                promedio_ms = sum(duraciones) / len(duraciones)
                promedio_min = promedio_ms / 60000  # convertir a minutos
                if promedio_min <= duracion_max_min:
                    filtrados.append(p)
            posibles = filtrados

        return posibles




