# database_config.py
from dotenv import load_dotenv
import os
import mongoengine

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_HOST'),
        'db': os.getenv('MONGODB_DB'),
        'tls': True,  # Para conexiones seguras
        # Puedes agregar otros parámetros como usuario, contraseña, etc.
    }

def init_db():
    """Inicializa la conexión a MongoDB usando la configuración definida."""
    config = Config()
    settings = config.MONGODB_SETTINGS
    mongoengine.connect(
        db=settings['db'],
        host=settings['host'],
        tls=settings['tls']
    )

db = mongoengine