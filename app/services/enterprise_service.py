from app.database.models.enterprise import Enterprise
from app.utils.logger import logger
from datetime import datetime, timedelta

class enterprise_service():

    logs = logger().get_logger()


    def create_enterprise(self):
        try:    
            hoy = datetime.today()
            # Crear el evento con los lotes procesados
            enterprise = Enterprise(
                access_time = hoy + timedelta(days=30),

            )
    
            if enterprise.save():
                return enterprise
        except Exception as e:
            self.logs.warning(e)
            return False
        
    def add_user_to_enterprise(self, enterprise_id, user):
        try:    
            
            empresa = Enterprise.objects(id=enterprise_id).first()
            if empresa.users is None:
                empresa.users = []
            empresa.users.append(user)
    
            if empresa.save():
                return empresa
        except Exception as e:
            self.logs.warning(e)
            return False

    def add_field_to_enterprise(self, empresa, field):
        try:    
            if empresa.fields is None:
                empresa.fields = []
            empresa.fields.append(field)
    
            if empresa.save():
                return empresa
        except Exception as e:
            self.logs.warning(e)
            return False            

    def extender_access_time(enterprise):
        try:
            enterprise.access_time += timedelta(days=30)
            enterprise.save()
            return {"message": "access_time extendido 30 días correctamente."}, 200
        except Enterprise.DoesNotExist:
            return {"error": "Empresa no encontrada."}, 404
        except Exception as e:
            return {"error": str(e)}, 500        
        
    def add_animals(self, enterprise, cantidad):
        try:
            enterprise.animals_in_fields += cantidad
            enterprise.save()
            self.logs.info('Se agregaron los animales a la empresa')
            return True
        except Enterprise.DoesNotExist:
            self.logs.debug("Empresa no encontrada.")
            return False
        except Exception as e:
            self.logs.debug("error "+ str(e))
            return False

