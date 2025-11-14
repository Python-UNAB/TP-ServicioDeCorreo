"""Gestión de filtros automáticos de mensajes."""
from typing import Callable, List


class GestorFiltros:
	"""Clase para gestionar filtros automáticos de usuarios."""
	
	@staticmethod
	def crear_filtro_asunto(palabra_clave: str) -> Callable:
		"""
		Crea un filtro que busca una palabra clave en el asunto.
		
		Args:
			palabra_clave: Texto a buscar (case-insensitive)
		
		Returns:
			Función de filtrado
		"""
		palabra_lower = palabra_clave.lower()
		return lambda mensaje: palabra_lower in mensaje.mostrar_asunto.lower()
	
	@staticmethod
	def crear_filtro_remitente(remitente: str) -> Callable:
		"""
		Crea un filtro que verifica el remitente.
		
		Args:
			remitente: Nombre de usuario del remitente
		
		Returns:
			Función de filtrado
		"""
		return lambda mensaje: mensaje.mostrar_remitente == remitente
	
	@staticmethod
	def crear_filtro_urgente() -> Callable:
		"""
		Crea un filtro para mensajes urgentes.
		
		Returns:
			Función que verifica si el mensaje es urgente
		"""
		return lambda mensaje: mensaje.es_urgente
	
	@staticmethod
	def agregar_filtro_usuario(usuario, nombre: str, condicion: Callable, 
	                           destino: str, crear_destino: bool = True):
		"""
		Agrega un filtro a un usuario.
		
		Args:
			usuario: Instancia de Usuario
			nombre: Nombre identificador del filtro
			condicion: Función que evalúa si un mensaje cumple el criterio
			destino: Ruta de carpeta destino
			crear_destino: Si debe crear la carpeta destino si no existe
		
		Complejidad: O(1)
		"""
		usuario.agregar_filtro(nombre, condicion, destino, crear_destino=crear_destino)
	
	@staticmethod
	def quitar_filtro_usuario(usuario, nombre: str) -> bool:
		"""
		Elimina un filtro de un usuario.
		
		Complejidad: O(f) donde f es el número de filtros
		"""
		return usuario.quitar_filtro(nombre)
	
	@staticmethod
	def listar_filtros_usuario(usuario) -> List[str]:
		"""
		Lista los filtros activos de un usuario.
		
		Complejidad: O(f) donde f es el número de filtros
		"""
		return usuario.listar_filtros()
