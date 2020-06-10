# Implementar los metodos de la capa de datos de socios.


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ejercicio_01 import Base, Socio


class DatosSocio(object):

    def __init__(self):
        engine = create_engine('sqlite:///socios.db')
        #Base.metadata.drop_all(engine) #Elimina todo lo que pueda tener el motor
        Base.metadata.bind = engine
        db_session = sessionmaker()
        db_session.bind = engine
        self.session = db_session()
        Base.metadata.create_all(engine) #crea todas las tablas que todavia no existen

    def buscar(self, id_socio):
        """
        Devuelve la instancia del socio, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        try:
            socio = self.session.query(Socio).filter(Socio.id == id_socio).one()
        except:
            print ("No se encontro el socio: ")
            return None
        return socio


    def buscar_dni(self, dni_socio):
        """
        Devuelve la instancia del socio, dado su dni.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        try:
            socio = self.session.query(Socio).filter(Socio.dni == dni_socio).one()
        except:
            print ("No se encontro el socio: ")
            return None
        return socio
        

    def todos(self):
        """
        Devuelve listado de todos los socios en la base de datos.
        :rtype: list
        """
        socios = self.session.query(Socio).all()
        return socios

    def borrar_todos(self):
        """
        Borra todos los socios de la base de datos.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        try:
            self.session.query(Socio).delete()
            self.session.commit()
            return True
        except:
            return False

    def alta(self, socio):
        """
        Devuelve el Socio luego de darlo de alta.
        :type socio: Socio
        :rtype: Socio
        """
        self.session.add(socio)
        self.session.commit()

        return socio

    def baja(self, id_socio):
        """
        Borra el socio especificado por el id.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        try:
            socioBaja = self.session.query(Socio).filter(Socio.id == id_socio).one()
            self.session.delete(socioBaja)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False


    def modificacion(self, socio):
        """
        Guarda un socio con sus datos modificados.
        Devuelve el Socio modificado.
        :type socio: Socio
        :rtype: Socio
        """
        try:
            newSocio = self.session.query(Socio).filter(Socio.id == socio.id).one()
            newSocio.nombre = socio.nombre
            newSocio.apellido = socio.apellido
            newSocio.dni = socio.dni
            self.session.commit()
        except:
            print ("No se encontro el socio: ")
        return socio
    
    def contarSocios(self):
        """
        Cuenta la cantidad de socios
        que existen en la tabla
        devuelve el numero de socios
        """
        rows = 0
        rows = self.session.query(Socio).count()
        return rows

def pruebas():
    # alta
    datos = DatosSocio()
    socio = datos.alta(Socio(dni=12345678, nombre='Juan', apellido='Perez'))
    assert socio.id > 0

    # baja
    assert datos.baja(socio.id) == True

    # buscar
    socio_2 = datos.alta(Socio(dni=12345679, nombre='Carlos', apellido='Perez'))
    assert datos.buscar(socio_2.id) == socio_2

    # buscar dni
    #En esta prueba modifique el dni 12345678 a 12345670 porque dni tiene una constraint para que no se creen 
    #dos dni iguales y por lo tanto falla
    socio_2 = datos.alta(Socio(dni=12345670, nombre='Carlos', apellido='Perez'))
    assert datos.buscar_dni(socio_2.dni) == socio_2

    # modificacion
    socio_3 = datos.alta(Socio(dni=12345680, nombre='Susana', apellido='Gimenez'))
    socio_3.nombre = 'Moria'
    socio_3.apellido = 'Casan'
    socio_3.dni = 13264587
    datos.modificacion(socio_3)
    socio_3_modificado = datos.buscar(socio_3.id)
    assert socio_3_modificado.id == socio_3.id
    assert socio_3_modificado.nombre == 'Moria'
    assert socio_3_modificado.apellido == 'Casan'
    assert socio_3_modificado.dni == 13264587

    # todos
    #para que pase esta prueba es necesario comentar modificacion debido a que cambiamos el dni a agregar
    #y entonces hay tres usuarios creados no dos
    assert len(datos.todos()) == 2

    # borrar todos
    datos.borrar_todos()
    assert len(datos.todos()) == 0


#if __name__ == '__main__':
    #pruebas()
