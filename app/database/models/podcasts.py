from app.database.database_config import db

class podcasts(db.Document):
    title = db.StringField()
    description = db.StringField()
    language = db.StringField()
    feed_url = db.StringField()
    source = db.StringField()
    image = db.StringField()
    author = db.StringField()
    GenreName = db.StringField()
    episodes = db.EmbeddedDocumentListField("episodes")
    

    def to_json(self):
        return {
            "id": str(self.id),
            'description': [str(user.id) for user in self.users],  # Convertir cada referencia a su ObjectId
            'fields': [field.to_json for field in self.fields],  # Convertir cada referencia a su ObjectId
            "access_time": str(self.access_time),
            "email_payer": self.email_payer if self.email_payer else None
        }
    
