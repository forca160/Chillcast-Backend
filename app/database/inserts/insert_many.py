
from database.models.pasture_types import Pastures_Types
from database_config import db

class Pastures_Types(db.Document):
    nombre = db.StringField(required=True, max_length=50)


    def to_json(self):
        return {
            'nombre': self.nombre
            }


# Lista de documentos a insertar
pastures_list = [
    {"nombre": "Bubalino"},
    {"nombre": "Porcino"},
    {"nombre": "Equino"},
    {"nombre": "Vacuno"},
    {"nombre": "Ovino"}
]


# Insertar documentos usando un bucle
for pasture_data in pastures_list:
    pasture = Pastures_Types(**pasture_data)
    pasture.save()

#python -m app.database.inserts.insert_many
print("Documentos insertados exitosamente.")

