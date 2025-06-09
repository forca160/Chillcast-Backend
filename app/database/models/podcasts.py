from app.database.database_config import db
from app.database.models.episodes import episodes

class podcasts(db.Document):
    title = db.StringField()
    description = db.StringField()
    language = db.StringField()
    feed_url = db.StringField()
    source = db.StringField()
    image = db.StringField()
    author = db.StringField()
    GenreName = db.StringField()
    episodes = db.ListField(db.ReferenceField(episodes))
    genero = db.ListField(db.StringField())
    autores = db.ListField(db.StringField())

    def to_json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            'description': self.description,  # Convertir cada referencia a su ObjectId
            "language": self.language,
            "feed_url": self.feed_url,
            "source": self.source,
            "image": self.image,
            "generos": self.genero,
            "autores": self.autores
        }
    
