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
        # 1) Filtros directos en Mongo
        query = Q()
        if 'title' in filtros:
            query &= Q(title__icontains=filtros['title'])
        if 'source' in filtros:
            query &= Q(source__icontains=filtros['source'])
        if 'generos' in filtros:
            query &= Q(genero__all=filtros['generos'])

        posibles = list(podcasts.objects(query))

        # 2) Filtro por autor (en Python)
        if 'autores' in filtros:
            autor_buscado = filtros['autores'].lower()
            posibles = [
                p for p in posibles
                if any(autor_buscado in autor.lower() for autor in p.autores)
            ]

        # 3) Filtro por RANGO de duración promedio de primeros 3 episodios
        dur_min = filtros.get('duracion_min')
        dur_max = filtros.get('duracion_max')
        if dur_min is not None or dur_max is not None:
            filtrados = []
            for p in posibles:
                eps = p.episodes[:3]
                if not eps:
                    continue
                # calculamos promedio en minutos
                ms_vals = [ep.duration_ms for ep in eps if getattr(ep, 'duration_ms', None)]
                if not ms_vals:
                    continue
                prom_min = sum(ms_vals) / len(ms_vals) / 60000
                # chequeo rango (si uno es None, sólo aplico el otro)
                if ((dur_min is None or prom_min >= dur_min) and
                    (dur_max is None or prom_min <= dur_max)):
                    filtrados.append(p)
            posibles = filtrados

        return posibles




