from ..algorithms.busqueda_recursiva import (
    buscar_mensajes_en_carpeta,
    extraer_mensajes_en_carpeta,
)
from ..algorithms.recorrido_grafo import bfs_carpeta, dfs_carpeta


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
        return buscar_mensajes_en_carpeta(self, criterio)

    def extraer_mensajes(self, criterio):
        """Extrae recursivamente mensajes que cumplen el criterio, eliminándolos de esta carpeta y subcarpetas."""
        return extraer_mensajes_en_carpeta(self, criterio)

    def recorrer(self):
        yield from self.recorrer_dfs()

    def recorrer_dfs(self):
        """Recorre la jerarquía en profundidad (DFS)."""
        yield from dfs_carpeta(self)

    def recorrer_bfs(self):
        """Recorre la jerarquía en amplitud (BFS)."""
        yield from bfs_carpeta(self)
