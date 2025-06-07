from flask import jsonify
from bson import ObjectId
from app.database.models.podcasts import podcasts
from app.database.models.episodes import episodes
import json

class jobs_service:

    def migrate_episodes(self):
        """
        Migra los episodios embebidos de cada Podcast a la colección 'episodes'
        y luego actualiza cada Podcast reemplazando el array embebido por
        la lista de ObjectId de los nuevos documentos.
        """
        coll = podcasts._get_collection()

        for raw in coll.find():
            embedded_eps = raw.get('episodes', [])
            if not embedded_eps:
                continue

            new_ids = []
            for ep_emb in embedded_eps:
                ep_doc = episodes(
                    title        = ep_emb.get('title'),
                    description  = ep_emb.get('description'),
                    duration_ms  = ep_emb.get('duration_ms'),
                    release_date = ep_emb.get('release_date'),
                    language     = ep_emb.get('language'),
                    image        = ep_emb.get('image'),
                    audio_url    = ep_emb.get('audio_url'),
                    # si NO tienes campo podcast en el modelo, no lo pases
                ).save()
                new_ids.append(ep_doc.id)

            # Sobrescribo directamente el campo 'episodes' con la nueva lista
            coll.update_one(
                {'_id': raw['_id']},
                {'$set': {'episodes': new_ids}}
            )

        return jsonify({"message": "Migración completada"}), 200
    



    def update_podcasts_with_genre_and_authors(self, json_path):
        """
        Lee un JSON local con una lista de documentos que incluyen _id.$oid (o 'id').
        Para cada ID:
        - Si no existe el campo 'autores', lo agrega como lista vacía.
        - Si no existe el campo 'genero' , lo agrega como lista vacía.
        """
        # Obtenemos la colección PyMongo
        coll = podcasts._get_collection()

        # Cargar JSON local
        with open(json_path, 'r', encoding='utf-8') as f:
            docs = json.load(f)

        updated = {"autores": 0, "genero": 0}
        for entry in docs:
            # Extraer el ID, ya sea bajo '_id.$oid' o bajo 'id'
            oid = None
            if isinstance(entry.get('_id'), dict):
                oid = entry['_id'].get('$oid')
            elif entry.get('id'):
                oid = entry['id']
            if not oid:
                continue

            try:
                obj_id = ObjectId(oid)
            except Exception:
                continue

            # Añadir 'autores' si falta
            res1 = coll.update_one(
                {'_id': obj_id, 'autores': {'$exists': False}},
                {'$set': {'autores': []}}
            )
            updated["autores"] += res1.modified_count

            # Añadir 'genero' si falta
            res2 = coll.update_one(
                {'_id': obj_id, 'genero':  {'$exists': False}},
                {'$set': {'genero': []}}
            )
            updated["genero"] += res2.modified_count

        print(f"Campos inicializados: autores={updated['autores']}, genero={updated['genero']}")
        return updated