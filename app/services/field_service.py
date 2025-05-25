from app.database.models.fields import Fields
from app.utils.logger import logger

class field_service():

    logs = logger().get_logger()


    def create_field(self, nombre, user=None):
        try:
            if user != None:
                field = Fields(
                    nombre=nombre,
                    users=[user]
                )
            else:
                field = Fields(
                    nombre=nombre
                )
    
            if field.save():
                return field
        except Exception as e:
            self.logs.warning(e)
            return False

    def agregar_usuario_al_campo(self, field_id, user):
        """
        Agrega el usuario (instancia de Users) al documento Fields identificado por field_id.
        Si el campo 'users' no existe o es None, lo inicializa como lista.
        Se evita agregar duplicados.
        """
        # Buscar el documento Fields por su id
        field = Fields.objects(id=field_id).first()
        if not field:
            raise Exception(f"No se encontró el Field con id {field_id}")
    
        # Asegurar que el campo 'users' esté inicializado (aunque debería ser una lista por defecto)
        if field.users is None:
            field.users = []

        # Si el usuario aún no está en la lista, se agrega
        if user not in field.users:
            field.users.append(user)
            field.save()

    def serialize_field(self, field):
        return {
            'id': str(field.id),  # Asegurarte de convertir ObjectId a string
            'nombre': field.nombre
        }

    def serialize_lote(self, lote):
        # Ajustar según las propiedades de los objetos de la clase Lotes
        return {
            'fecha_vencimiento': lote.fecha_vencimiento.isoformat() if lote.fecha_vencimiento else None,
            'nombre': lote.nombre,
            'cupos': lote.cupos,
            'precio': lote.precio,
            'entradas_vendidas': lote.entradas_vendidas
            # Agregar más campos según sea necesario
        }
           
    def get_fields(self):
        documentos = Fields.objects()  # Esto obtiene todos los documentos de la colección
        campos_serializados = [self.serialize_field(doc) for doc in documentos]
        return {'documentos': campos_serializados}
    
    def get_field_by_id(self, id_campo):
        try:
            campo = Fields.objects(id=id_campo).first()
            if campo:
                self.logs.debug(f"Campo encontrado: {campo}")
                return campo
            else:
                self.logs.warning(f"Campo con ID {id_campo} no encontrado.")
                return None
        except Exception as e:
            self.logs.error(f"Error al buscar Campo por ID {id_campo}: {e}")
            raise    

    def get_fields_by_idUser(self, id_campo):
        try:
            campo = Fields.objects(id=id_campo).first()
            if campo:
                self.logs.debug(f"Campo encontrado: {campo}")
                return campo
            else:
                self.logs.warning(f"Campo con ID {id_campo} no encontrado.")
                return None
        except Exception as e:
            self.logs.error(f"Error al buscar Campo por ID {id_campo}: {e}")
            raise  

    def campo_por_nombre(self, nombre):
        try:
            campo = Fields.objects(nombre=nombre).first()
            if campo:
                self.logs.debug(f"Campo encontrado: {campo}")
                return campo
            else:
                self.logs.warning(f"Campo con nombre {nombre} no encontrado.")
                return None
        except Exception as e:
            self.logs.error(f"Error al buscar Campo por nombre {nombre}: {e}")
            raise     

    def agregar_potrero_campo(self, campo, potrero):
        try:
            campo.pasture.append(potrero)
            campo.save()
            self.logs.info('Se agrego el potrero al campo')
        except Exception as e:
            self.logs.error(f"Error al intentar agregar el potrero al campo: {e}")
            raise     

    def add_enterprise_to_field(self, campo, empresa):
        try: 
            campo.enterprise = empresa
            campo.save()
            return campo
        except Exception as e:
            self.logs.error(f"Error al intentar agregar la empresa al campo: {e}")
            raise     
    
    """    def delete_event(self, id_evento):
            try:
                # Buscar el evento en la base de datos
                evento = Eventos.objects(id=id_evento).first()
                self.logs.debug(evento)

                if not evento:
                    self.logs.warning(f"No se encontró el evento con ID: {id_evento}")
                    return False

                # Verificar si hay entradas asociadas al evento
                entradas_vendidas = Entradas.objects(evento=evento).count()
                if entradas_vendidas > 0:
                    # Si hay entradas, marcar el evento como inactivo
                    evento.estado = "inactivo"
                    evento.save()
                    self.logs.info(f"El evento con ID {id_evento} tiene entradas vendidas y se marcó como inactivo.")
                    return "inactivo"
                else:
                    # Si no hay entradas, eliminar el evento
                    if evento.ruta_flyer:
                        public_id = evento.ruta_flyer.split("/")[-1].split(".")[0]  # Extraer el public_id
                        if eliminar_imagen(public_id):
                            self.logs.info(f"Imagen con public_id '{public_id}' eliminada de Cloudinary.")
                        else:
                            self.logs.warning(f"No se pudo eliminar la imagen con public_id '{public_id}' de Cloudinary.")

                    # Eliminar usuarios vinculados al evento
                    usuarios_eliminados = Users.objects(evento=evento).delete()
                    self.logs.info(f"{usuarios_eliminados} usuarios eliminados vinculados al evento {id_evento}.")

                    # Eliminar el evento
                    evento.delete()
                    self.logs.info(f"El evento con ID {id_evento} se eliminó correctamente.")
                    return "eliminado"
            except Exception as e:
                self.logs.error(f"Error al eliminar el evento {id_evento}: {e}")
                return False
            
        def modificar_evento(self, evento, datos):
            try:
                atributos_a_cambiar = {}

                # Manejar el campo "lotes" si está presente en los datos
                nuevos_lotes = datos.get("lotes")
                if nuevos_lotes:
                    if isinstance(nuevos_lotes, str):  # Solo intentar cargarlo si es un string
                        try:
                            nuevos_lotes = json.loads(nuevos_lotes)  # Convertir el JSON string a una lista de diccionarios
                        except json.JSONDecodeError:
                            self.logs.warning('El campo "lotes" no es un JSON válido.')
                            return False

                    if isinstance(nuevos_lotes, list):  # Asegurarse de que es una lista antes de procesar
                        lotes_actuales = {lote.nombre: lote for lote in evento.lotes}  # Índice por nombre
                        lotes_actualizados = []

                        for nuevo_lote in nuevos_lotes:
                            nombre = nuevo_lote.get("nombre")
                            if not nombre:
                                continue  # Saltar lotes sin nombre

                            if nombre in lotes_actuales:
                                # Si el lote ya existe, actualizamos sus campos
                                lote_existente = lotes_actuales[nombre]
                                lote_existente.precio = nuevo_lote.get("precio", lote_existente.precio)
                                lote_existente.cupos = nuevo_lote.get("cupos", lote_existente.cupos)
                                lote_existente.fecha_vencimiento = nuevo_lote.get(
                                    "fecha_vencimiento", lote_existente.fecha_vencimiento
                                )
                                lotes_actualizados.append(lote_existente)
                            else:
                                # Si es un lote nuevo, inicializar entradas_vendidas a 0
                                lote_nuevo = Lotes(
                                    nombre=nombre,
                                    precio=nuevo_lote.get("precio"),
                                    cupos=nuevo_lote.get("cupos"),
                                    fecha_vencimiento=nuevo_lote.get("fecha_vencimiento"),
                                    entradas_vendidas=0  # Nuevo lote, entradas vendidas inicializadas a 0
                                )
                                lotes_actualizados.append(lote_nuevo)

                        evento.lotes = lotes_actualizados  # Actualizar los lotes del evento
                        atributos_a_cambiar["lotes"] = evento.lotes
                    else:
                        self.logs.warning('El campo "lotes" no es una lista válida.')
                        return False

                # Manejar otros atributos del evento
                for atributo in evento._fields:
                    if atributo in datos and atributo != "id" and atributo != "lotes":  # Ignorar 'id' y 'lotes'
                        atributos_a_cambiar[atributo] = datos[atributo]

                # Guardar los cambios en el evento si hay algo que actualizar
                if atributos_a_cambiar:
                    evento.modify(**atributos_a_cambiar)
                    return True
                else:
                    return False
            except Exception as e:
                self.logs.warning('Hubo un inconveniente al guardar el evento.')
                self.logs.warning(e)
                return False

        def obtener_eventos_por_organizador(self, organizador_id):
            try:
                # Filtrar los eventos creados por el organizador
                documentos = Eventos.objects(created_by=str(organizador_id))
                # Serializar los eventos
                eventos_serializados = [self.serialize_event(doc) for doc in documentos]
                return {"documentos": eventos_serializados}
            except Exception as e:
                self.logs.error(f"Error al obtener eventos por organizador: {e}")
                return {"documentos": []}
        
        def obtener_ganancias_netas(self, id_evento): #devuelve las ganancias del evento al organizador
            try:
                # Obtener el evento correspondiente al ID
                evento = Eventos.objects(id=id_evento).first()
                if not evento:
                    return {"error": "Evento no encontrado"}
                
                # Crear un diccionario con los precios de los lotes por nombre
                precios_lotes = {}
                for lote in evento.lotes:
                    #cobrado = lote['precio'] + lote['precio']*evento.comision
                    porc_comision_mp = 0.0629
                    porc_iva = 0.21
                    comision_mp = lote['precio']*porc_comision_mp
                    iva = comision_mp*porc_iva
                    
                    precios_lotes[lote["nombre"]] = lote['precio'] - comision_mp - iva
                    precios_lotes[lote["nombre"]] = precios_lotes[lote["nombre"]] - (precios_lotes[lote["nombre"]] * (evento.comision/100))

                # Consultar las entradas asociadas al evento
                entradas = Entradas.objects(evento=id_evento)

                # Calcular el total sumando los precios de los lotes relacionados con cada entrada
                total = round(sum(precios_lotes.get(entrada.lote, 0) for entrada in entradas),2)

                return {"total": total}
            except Exception as e:
                return {"error": str(e)}

        def obtener_comisiones(self, id_evento): #devuelve las ganancias de la comision de Almotick

        try:
            # Obtener el evento correspondiente al ID
            evento = Eventos.objects(id=id_evento).first()
            if not evento:
                return {"error": "Evento no encontrado"}
            
            # Crear un diccionario con los precios de los lotes por nombre
            precios_lotes = {}
            for lote in evento.lotes:
                #cobrado = lote['precio'] + lote['precio']*evento.comision
                porc_comision_mp = 0.0629
                porc_iva = 0.21
                comision_mp = lote['precio']*porc_comision_mp
                iva = comision_mp*porc_iva
                
                precios_lotes[lote["nombre"]] = lote['precio'] - comision_mp - iva
                precios_lotes[lote["nombre"]] = precios_lotes[lote["nombre"]] * (evento.comision/100)

            # Consultar las entradas asociadas al evento
            entradas = Entradas.objects(evento=id_evento)

            # Calcular el total sumando los precios de los lotes relacionados con cada entrada
            total = round(sum(precios_lotes.get(entrada.lote, 0) for entrada in entradas),2)

            return {"total": total}
        except Exception as e:
            return {"error": str(e)}"""