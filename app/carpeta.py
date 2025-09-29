class Carpeta:
    def __init__(self, nombre_carpeta):
        self.__nombre_carpeta = nombre_carpeta
        self.__mensajes = []   #lista de Mensajes (objeto)
    
    @property
    def nombre(self):
        return self.__nombre_carpeta

    def agregar_mensaje(self, mensaje):
        self.__mensajes.append(mensaje)

    def listar_mensajes(self):
        return [m.mostrar_resumen() for m in self.__mensajes]