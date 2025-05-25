from app.database.database_config import db
from app.database.models.animals.animals import Animals

class Pastures(db.Document):
    name = db.StringField(required=True, max_length=50)
    field = db.ReferenceField('Fields', required=True)
    animals = db.EmbeddedDocumentListField(Animals)

    def to_json(self):
        return {
            "id": str(self.id),
            'field': str(self.field.id),
            'name': self.name,
            'animals': [animal.to_json() for animal in self.animals], # Convertir cada animal a JSON
            }

