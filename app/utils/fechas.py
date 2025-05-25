import datetime

class fechas():

    def convertir_a_datetime(self, fecha_str):
        """
        Convierte una cadena en el formato "hora:minutos:segundos dia/mes/año"
        a un objeto datetime, adecuado para asignarlo a un DateTimeField de MongoEngine.
        
        Ejemplo:
            fecha_str = "15:30:25 01/04/2025"
            retorna: datetime.datetime(2025, 4, 1, 15, 30, 25)
        """
        try:
            fecha_dt = datetime.datetime.strptime(fecha_str, "%H:%M:%S %d/%m/%Y")
            return fecha_dt
        except ValueError as e:
            # En caso de formato incorrecto se puede manejar la excepción como se necesite
            print(f"Error en el formato de fecha: {e}")
            return None

    """ Ejemplo de uso:
        fecha_input = "15:30:25 01/04/2025"""

