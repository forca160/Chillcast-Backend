import os
import logging

class logger:

    ruta_file_log = os.path.join('app', 'utils', 'log', 'app.log')

    def __init__(self):
        # Configura una única instancia de logger
        self.logger = logging.getLogger("logger_test")
        if not self.logger.hasHandlers():  # Evita agregar múltiples handlers
            self._ensure_log_directory_exists()
            self._set_logger()

    def _ensure_log_directory_exists(self):
        # Asegúrate de que el directorio para logs exista
        log_directory = os.path.dirname(self.ruta_file_log)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory, exist_ok=True)

    def _set_logger(self):
        # Configuración básica de logging
        logging.basicConfig(
            level=logging.DEBUG,  # Configura el nivel de registro
            format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',
            filename=self.ruta_file_log,
        )

        # Establece el nivel para el logger
        self.logger.setLevel(logging.DEBUG)

        # Crea un handler para la consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Formato para el handler de consola
        console_format = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)

        # Crea un handler para archivo
        file_handler = logging.FileHandler(self.ruta_file_log)
        file_handler.setLevel(logging.ERROR)

        # Formato para el handler de archivo
        file_format = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        # Agrega los handlers al logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
