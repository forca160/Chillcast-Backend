from app.database.database_config import db
from werkzeug.security import generate_password_hash, check_password_hash



class Users(db.Document):
    username = db.StringField(required=True, max_length=60, unique=True)
    email = db.StringField(required=True, max_length=60, unique=True)
    password = db.StringField(required=True)
    nombre = db.StringField(required=True)
    apellido = db.StringField(required=True)
    fecha_alta = db.DateTimeField(auto_now_add=True)
    generos_fav = db.ListField(db.ReferenceField('podcasts'))
    history = db.ListField(db.ReferenceField('podcasts'))
    activo = db.BooleanField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_alta": self.fecha_alta.isoformat() if self.fecha_alta else None,
            "history": [f.to_json() for f in self.history] if len(self.history)>=0 else None,
            "generos_fav": self.generos_fav if self.generos_fav else None,
            "activo": self.activo
        }

