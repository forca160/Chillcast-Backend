from app.database.models.users import Users
from app.utils.logger import logger
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
class user_service():

    logs = logger().get_logger()

    def create_user(self, email, password, rol, nombre, apellido, telefono, fields, enterprise):
        # Verificar si el usuario ya está registrado
        if Users.objects(email=email).first():
            raise ValueError("El usuario ya está registrado")

        # Crear un nuevo usuario
        user = Users(
            email=email,
            nombre=nombre,
            password=password,
            rol=rol,
            apellido=apellido,
            telefono=telefono,
            fields=[fields], 
            enterprise=enterprise
        )
        user.save()
        return user

    def edit_user(self, user, data):
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)    

        user.save()
        return user
    
    def verify_user(email, password):
        # Busca al usuario por el nombre de usuario
        user = Users.objects(email=email).first()
        if not user:
            return False

        # Verifica si la contraseña está hasshead y es correcta
        if not bcrypt.check_password_hash(user.password, password):
            return False
        
        return user
    
    def check_duplicate_usernames(self, usernames):
        try:
            # Buscar usernames duplicados en la base de datos
            existing_users = Users.objects(username__in=usernames).only("username")
            duplicates = [user.username for user in existing_users]
            return duplicates
        except Exception as e:
            self.logs.error(f"Error al verificar usuarios duplicados: {e}")
            raise RuntimeError("Error al verificar usuarios duplicados") from e

    def get_user_by_email(self, email):
        return Users.objects(email=email).first()
    
    def get_user_by_id(self, id_user):
        return Users.objects(id=id_user).first()

    def get_users_by_enterprise(self, enterprise):
        return Users.objects(enterprise=enterprise)
                
    def add_field_to_user(self, field, user):
        try:
            user.fields.append(field)
            user.save()
            print(user.email)
            self.logs.info('Se guardó el campo en el usuario')
            return True
        except Exception as e:
            self.logs.warning(e)
            return False
        
