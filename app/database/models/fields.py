from app.database.database_config import db

class Fields(db.Document):
    nombre = db.StringField(required=True, max_length=50)
    users = db.ListField(db.ReferenceField('Users'))
    pasture = db.ListField(db.ReferenceField('Pastures'))

    def to_json(self):
        return {
            "id": str(self.id),
            'nombre': self.nombre,
            'users': [str(user.id) for user in self.users],  # Convertir cada referencia a su ObjectId
            'pasture': [pasture.to_json() for pasture in self.pasture]
        }
    
    