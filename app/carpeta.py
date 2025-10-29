class Carpeta:
    """Representa una carpeta que puede contener mensajes y subcarpetas."""

    def __init__(self, nombre_carpeta):
        self.__nombre_carpeta = nombre_carpeta
        self.__mensajes = []  # Lista de Mensajes
        self.__subcarpetas = {}  # nombre -> Carpeta

    @property
    def nombre(self):
        return self.__nombre_carpeta

    def agregar_mensaje(self, mensaje):
        self.__mensajes.append(mensaje)

    def agregar_mensajes(self, mensajes):
        self.__mensajes.extend(mensajes)

    def listar_mensajes(self):
        return list(self.__mensajes)

    def eliminar_mensaje(self, mensaje):
        try:
            self.__mensajes.remove(mensaje)
            return True
        except ValueError:
            return False

    def crear_subcarpeta(self, nombre):
        if nombre not in self.__subcarpetas:
            self.__subcarpetas[nombre] = Carpeta(nombre)
        return self.__subcarpetas[nombre]

    def obtener_subcarpeta(self, nombre):
        return self.__subcarpetas.get(nombre)

    def listar_subcarpetas(self):
        return dict(self.__subcarpetas)

    def buscar_mensajes(self, criterio):
        """Busca recursivamente mensajes que cumplen el criterio en esta carpeta y todas sus subcarpetas."""
        encontrados = [m for m in self.__mensajes if criterio(m)]
        # Recursión: buscar en cada subcarpeta
        for subcarpeta in self.__subcarpetas.values():
            encontrados.extend(subcarpeta.buscar_mensajes(criterio))
        return encontrados

    def extraer_mensajes(self, criterio):
        """Extrae recursivamente mensajes que cumplen el criterio, eliminándolos de esta carpeta y subcarpetas."""
        retenidos = []
        extraidos = []
        for mensaje in self.__mensajes:
            if criterio(mensaje):
                extraidos.append(mensaje)
            else:
                retenidos.append(mensaje)
        self.__mensajes = retenidos
        # Recursión: extraer también de subcarpetas
        for subcarpeta in self.__subcarpetas.values():
            extraidos.extend(subcarpeta.extraer_mensajes(criterio))
        return extraidos

    def recorrer(self):
        yield self
        for subcarpeta in self.__subcarpetas.values():
            yield from subcarpeta.recorrer()