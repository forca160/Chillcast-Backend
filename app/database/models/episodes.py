from app.database.database_config import db


class episodes(db.Document):
    title = db.StringField()
    description = db.StringField()
    duration_ms = db.IntField()
    release_date = db.StringField()
    language = db.StringField()
    image = db.StringField()
    audio_url = db.StringField()
    

    def to_json(self):
        return {
            "id": str(self.id),
            'field': str(self.field.id),
            'name': self.name,
            'animals': [animal.to_json() for animal in self.animals], # Convertir cada animal a JSON
            }

