from app.database.database_config import db
from werkzeug.security import generate_password_hash, check_password_hash



class Users(db.Document):
    email = db.StringField(required=True, max_length=60, unique=True)
    password = db.StringField(required=True)
    nombre = db.StringField(required=True)
    apellido = db.StringField(required=True)
    created_at = db.DateTimeField(auto_now_add=True)
    favorites = db.ListField(db.ReferenceField('podcasts'))
    history = db.ListField(db.ReferenceField('podcasts'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "firstname": self.nombre,
            "lastname": self.apellido,
            "rol": self.rol,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "favorites": [f.to_json() for f in self.favorites] if self.history else None,
        }

