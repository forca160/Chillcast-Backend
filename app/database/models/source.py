from app.database.database_config import db


class source(db.Document):
    source_name = db.StringField()
    

    def to_json(self):
        return {
            'source': self.source_name
            }

