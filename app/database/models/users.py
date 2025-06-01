from app.database.database_config import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.models.fields import Fields


class Users(db.Document):
    email = db.StringField(required=True, max_length=60, unique=True)
    password = db.StringField(required=True)
    nombre = db.StringField(required=True)
    apellido = db.StringField(required=True)
    created_at = db.DateTimeField(auto_now_add=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id": str(self.id),
            "mail": self.email,
            "firstname": self.nombre,
            "lastname": self.apellido,
            "rol": self.rol,
            "fields": [
                str(field.id) for field in self.fields
            ],  # o field.to_json() si tenés método
            "enterprise": str(self.enterprise.id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def fields_to_json(self):
        result = []
        for field in self.fields:
            try:
                result.append(field.to_json())
            except Exception as e:
                print(f"Error al convertir field a json: {field} - {e}")
        return {"fields": result}
