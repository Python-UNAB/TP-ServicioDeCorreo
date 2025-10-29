from typing import Callable, Dict, List, Optional

from .carpeta import Carpeta


class Usuario:
	def __init__(self, username: str, password: str):
		"""Crea un usuario con carpetas raíz por defecto y reglas de filtrado."""
		self.__username = username
		self.__password = password
		self.__carpetas: Dict[str, Carpeta] = {}
		self.__filtros: List[Dict[str, object]] = []
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
		# Navegar recursivamente por subcarpetas
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

	def listar_carpetas(self) -> List[str]:
		rutas = []
		for nombre, carpeta in sorted(self.__carpetas.items()):
			rutas.extend(self.__listar_recursivo(carpeta, nombre))
		return rutas

	def __listar_recursivo(self, carpeta: Carpeta, prefijo: str) -> List[str]:
		rutas = [prefijo]
		for nombre, subcarpeta in sorted(carpeta.listar_subcarpetas().items()):
			rutas.extend(self.__listar_recursivo(subcarpeta, f"{prefijo}/{nombre}"))
		return rutas

	def buscar_mensajes(self, criterio: Callable, carpeta_ruta: Optional[str] = None):
		"""Busca mensajes que cumplen el criterio en la carpeta especificada o en todas."""
		if carpeta_ruta:
			carpeta = self.obtener_carpeta(carpeta_ruta)
			if carpeta is None:
				return []
			return carpeta.buscar_mensajes(criterio)
		# Buscar en todas las carpetas raíz
		resultados = []
		for carpeta in self.__carpetas.values():
			resultados.extend(carpeta.buscar_mensajes(criterio))
		return resultados

	def mover_mensajes(self, criterio: Callable, destino_ruta: str, origen_ruta: Optional[str] = None, *, crear_destino: bool = False) -> int:
		"""Mueve mensajes que cumplen el criterio desde el origen hacia el destino."""
		destino = self._navegar_ruta(destino_ruta, crear=crear_destino)
		if destino is None:
			raise ValueError("La carpeta destino no existe")
		# Determinar carpetas de origen
		fuentes = []
		if origen_ruta:
			carpeta_origen = self.obtener_carpeta(origen_ruta)
			if carpeta_origen is None:
				raise ValueError("La carpeta origen no existe")
			fuentes.append(carpeta_origen)
		else:
			fuentes = list(self.__carpetas.values())
		# Extraer y mover mensajes
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
		if any(filtro["nombre"] == nombre for filtro in self.__filtros):
			raise ValueError(f"Ya existe un filtro con el nombre {nombre}")
		self.__filtros.append({
			"nombre": nombre,
			"condicion": condicion,
			"destino": destino_ruta,
			"crear_destino": crear_destino,
		})

	def listar_filtros(self) -> List[str]:
		return [filtro["nombre"] for filtro in self.__filtros]

	def aplicar_filtros(self, mensaje) -> Optional[str]:
		"""Aplica filtros automáticos al mensaje recibido, moviéndolo si coincide con algún criterio."""
		entrada = self.obtener_carpeta("Entrada")
		if entrada is None:
			return None
		for filtro in self.__filtros:
			condicion = filtro["condicion"]
			if condicion(mensaje):
				destino = self._navegar_ruta(filtro["destino"], crear=filtro.get("crear_destino", False))
				if destino is None:
					continue
				# Mover mensaje de Entrada a la carpeta destino del filtro
				if entrada.eliminar_mensaje(mensaje):
					destino.agregar_mensaje(mensaje)
					return filtro["nombre"]
		return None