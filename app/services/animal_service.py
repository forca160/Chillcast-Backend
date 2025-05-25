from app.database.models.animals.animals import Animals
from app.database.models.animals.animal_category import Animals_Categories
from app.database.models.animals.animal_subcategory import Animals_Subcategories
from app.database.models.animals.animal_breed import Animals_Breed
from app.utils.logger import logger

class animal_service():

    logs = logger().get_logger()

    def agregar_animal(self, animal_type, animal_quantity):
        try:
            
            animal = Animals(
                animal_type=animal_type,
                animal_quantity=animal_quantity
            )
    
            if animal.save():
                return animal
        except Exception as e:
            self.logs.warning(e)
            return False
        
    def get_all_animals(self):
        documentos = Animals.objects()  # Esto obtiene todos los documentos de la colección
        animales_serializados = [doc.to_json() for doc in documentos]
        return {'documentos': animales_serializados}
    
    def embeber_animales(self, animal_category, animal_subcategory, animal_breed, animal_quantity):
        try:
            animales = Animals(
                animal_category=animal_category,
                animal_subcategory=animal_subcategory,
                animal_breed=animal_breed,
                animal_quantity=animal_quantity
            )
            return animales
        
        except Exception as e:
            self.logs.warning(e)
            return False
        
    def agregar_categoria_animal(self, categoria):
        try:
            
            categoria = Animals_Categories(
                animal_category=categoria
            )
    
            if categoria.save():
                return categoria
        except Exception as e:
            self.logs.warning(e)
            return False        
        
    def agregar_subcategoria_animal(self, categoria_animal, subcategoria):
        try:
            
            subcategoria = Animals_Subcategories(
                animal_category=categoria_animal,
                animal_subcategory=subcategoria
            )
    
            if subcategoria.save():
                return subcategoria
        except Exception as e:
            self.logs.warning(e)
            return False                
        
    def get_category_by_name(self, category_name):

        categoria = Animals_Categories.objects(animal_category=category_name).first()
        if categoria != None:
            return categoria
        else:
            return False
        
    def get_subcategory_by_name(self, subcategory_name):

        subcategoria = Animals_Subcategories.objects(animal_subcategory=subcategory_name).first()
        if subcategoria != None:
            return subcategoria
        else:
            return False        
        
    def get_subcategorys(self):
        subcategoria = Animals_Subcategories.objects()
        return subcategoria
