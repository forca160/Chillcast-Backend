from app.database.database_config import db

class Enterprise(db.Document):
    users = db.ListField(db.ReferenceField('Users'))
    fields = db.ListField(db.ReferenceField('Fields'))
    suscription_plan = db.ReferenceField('Suscription_Plan')
    animals_in_fields = db.IntField(default=0)
    access_time = db.DateTimeField(required=True)
    email_payer = db.StringField()
    

    def to_json(self):
        return {
            "id": str(self.id),
            'users': [str(user.id) for user in self.users],  # Convertir cada referencia a su ObjectId
            'fields': [field.to_json for field in self.fields],  # Convertir cada referencia a su ObjectId
            "access_time": str(self.access_time),
            "email_payer": self.email_payer if self.email_payer else None
        }
    
