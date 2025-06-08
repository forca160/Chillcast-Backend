from app.database.database_config import db


class genero(db.Document):
    nombre_genero = db.StringField()
    

    def to_json(self):
        return {
            "id": str(self.id),
            'name': self.nombre_genero
            }

