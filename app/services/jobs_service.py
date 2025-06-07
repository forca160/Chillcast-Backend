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
        Lee un JSON local donde cada objeto tiene:
            - "_id": {"$oid": "<hexid>"} o "id": "<hexid>"
            - "genero": [<string>, ...]
            - "autores": [<string>, ...]
        Y para cada entrada:
            • Convierte el ID a ObjectId.
            • Hace un $set de los valores de 'genero' y 'autores' tal cual aparecen en el JSON.
        """
        # Acceso directo a la colección PyMongo
        coll = podcasts._get_collection()

        # Cargo el JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            docs = json.load(f)

        stats = {"total": 0, "updated": 0}
        for entry in docs:
            # 1) Extraer el HexID
            oid = None
            if isinstance(entry.get("_id"), dict):
                oid = entry["_id"].get("$oid")
            elif entry.get("id"):
                oid = entry["id"]
            if not oid:
                continue

            try:
                obj_id = ObjectId(oid)
            except Exception:
                continue

            # 2) Preparar el $set con lo que venga en el JSON
            set_ops = {}
            if "genero" in entry and isinstance(entry["genero"], list):
                set_ops["genero"] = entry["genero"]
            if "autores" in entry and isinstance(entry["autores"], list):
                set_ops["autores"] = entry["autores"]

            if not set_ops:
                continue

            # 3) Ejecutar la actualización
            result = coll.update_one(
                {"_id": obj_id},
                {"$set": set_ops}
            )
            stats["total"] += 1
            if result.modified_count:
                stats["updated"] += 1

        print(f"Procesados: {stats['total']} entradas, actualizados: {stats['updated']}")
        return stats