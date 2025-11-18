import heapq
from collections import deque
from itertools import count
from typing import Callable, Dict, List, Optional, TYPE_CHECKING

from .carpeta import Carpeta
from .filtro import Filtro

if TYPE_CHECKING:
	from .mensaje import Mensaje

class Usuario:
	def __init__(self, username: str, password: str):
		"""Crea un usuario con carpetas raíz por defecto y reglas de filtrado."""
		self.__username = username
		self.__password = password
		self.__carpetas: Dict[str, Carpeta] = {}
		self.__filtros: List[Filtro] = []
		self.__cola_urgentes = []  # Heap (prioridad, orden, mensaje)
		self.__contador_urgentes = count()
		for nombre in ("Entrada", "Enviados"):
			self.__carpetas[nombre] = Carpeta(nombre)

	@property
	def username(self):
		return self.__username

	@property
	def password(self):
		return self.__password

	def _navegar_ruta(self, ruta: str, *, crear: bool) -> Optional[Carpeta]:
		"""Navega por una ruta de carpetas (ej: 'Entrada/Proyectos/2025'), creándolas si es necesario."""
		partes = [p for p in ruta.split("/") if p]
		if not partes:
			return None
		carpeta = self.__carpetas.get(partes[0])
		if carpeta is None and crear:
			carpeta = self.__carpetas.setdefault(partes[0], Carpeta(partes[0]))
		elif carpeta is None:
			return None
		for nombre in partes[1:]:
			siguiente = carpeta.obtener_subcarpeta(nombre)
			if siguiente is None:
				siguiente = carpeta.crear_subcarpeta(nombre) if crear else None
			if siguiente is None:
				return None
			carpeta = siguiente
		return carpeta

	def obtener_carpeta(self, ruta: str) -> Optional[Carpeta]:
		return self._navegar_ruta(ruta, crear=False)

	def obtener_o_crear_carpeta(self, ruta: str) -> Carpeta:
		carpeta = self._navegar_ruta(ruta, crear=True)
		if carpeta is None:
			raise ValueError("La ruta de carpeta no puede estar vacía")
		return carpeta

	def listar_carpetas(self, orden: str = "dfs") -> List[str]:
		"""Devuelve las rutas de carpetas usando recorrido DFS (default) o BFS."""
		rutas = []
		for nombre, carpeta in sorted(self.__carpetas.items()):
			if orden == "dfs":
				rutas.extend(self.__listar_recursivo(carpeta, nombre))
			elif orden == "bfs":
				rutas.extend(self.__listar_bfs(carpeta, nombre))
			else:
				raise ValueError("Orden de recorrido no soportado, use 'dfs' o 'bfs'")
		return rutas

	def __listar_recursivo(self, carpeta: Carpeta, prefijo: str) -> List[str]:
		rutas = [prefijo]
		for nombre, subcarpeta in sorted(carpeta.listar_subcarpetas().items()):
			rutas.extend(self.__listar_recursivo(subcarpeta, f"{prefijo}/{nombre}"))
		return rutas

	def __listar_bfs(self, carpeta: Carpeta, prefijo: str) -> List[str]:
		cola = deque([(carpeta, prefijo)])
		rutas = []
		while cola:
			actual, ruta = cola.popleft()
			rutas.append(ruta)
			subcarpetas = sorted(actual.listar_subcarpetas().items())
			for nombre, subcarpeta in subcarpetas:
				cola.append((subcarpeta, f"{ruta}/{nombre}"))
		return rutas

	def buscar_mensajes(self, criterio: Callable, carpeta_ruta: Optional[str] = None):
		"""Busca mensajes que cumplen el criterio en la carpeta especificada o en todas."""
		if carpeta_ruta:
			carpeta = self.obtener_carpeta(carpeta_ruta)
			if carpeta is None:
				return []
			return carpeta.buscar_mensajes(criterio)
		resultados = []
		for carpeta in self.__carpetas.values():
			resultados.extend(carpeta.buscar_mensajes(criterio))
		return resultados

	def mover_mensajes(self, criterio: Callable, destino_ruta: str, origen_ruta: Optional[str] = None, *, crear_destino: bool = False) -> int:
		"""Mueve mensajes que cumplen el criterio desde el origen hacia el destino."""
		destino = self._navegar_ruta(destino_ruta, crear=crear_destino)
		if destino is None:
			raise ValueError("La carpeta destino no existe")
		fuentes = []
		if origen_ruta:
			carpeta_origen = self.obtener_carpeta(origen_ruta)
			if carpeta_origen is None:
				raise ValueError("La carpeta origen no existe")
			fuentes.append(carpeta_origen)
		else:
			fuentes = list(self.__carpetas.values())
		movidos = 0
		for carpeta in fuentes:
			extraidos = carpeta.extraer_mensajes(criterio)
			if extraidos:
				movidos += len(extraidos)
				destino.agregar_mensajes(extraidos)
		if movidos == 0:
			raise LookupError("No se encontraron mensajes que coincidan con el criterio")
		return movidos

	def agregar_filtro(self, nombre: str, condicion: Callable, destino_ruta: str, *, crear_destino: bool = True):
		if any(filtro.nombre == nombre for filtro in self.__filtros):
			raise ValueError(f"Ya existe un filtro con el nombre {nombre}")
		self.__filtros.append(Filtro(nombre, condicion, destino_ruta, crear_destino=crear_destino))

	def listar_filtros(self) -> List[str]:
		return [filtro.nombre for filtro in self.__filtros]

	def aplicar_filtros(self, mensaje) -> Optional[str]:
		"""Aplica filtros automáticos al mensaje recibido, moviéndolo si coincide con algún criterio."""
		entrada = self.obtener_carpeta("Entrada")
		if entrada is None:
			return None
		for filtro in self.__filtros:
			if filtro.aplica_a(mensaje):
				destino = self._navegar_ruta(filtro.destino_ruta, crear=filtro.crear_destino)
				if destino is None:
					continue
				if entrada.eliminar_mensaje(mensaje):
					destino.agregar_mensaje(mensaje)
					return filtro.nombre
		return None

	def registrar_mensaje_urgente(self, mensaje: "Mensaje") -> None:
		"""Agrega el mensaje a la bandeja de urgentes del usuario."""
		prioridad = getattr(mensaje, "prioridad", None)
		if prioridad is None:
			return
		heapq.heappush(self.__cola_urgentes, (prioridad, next(self.__contador_urgentes), mensaje))

	def tiene_mensajes_urgentes(self) -> bool:
		return bool(self.__cola_urgentes)

	def extraer_mensaje_urgente(self):
		if not self.__cola_urgentes:
			return None
		return heapq.heappop(self.__cola_urgentes)[2]
