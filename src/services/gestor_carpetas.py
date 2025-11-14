"""Gestión de operaciones con carpetas."""
from typing import List, Tuple


class GestorCarpetas:
	"""Clase para gestionar operaciones sobre carpetas de usuarios."""
	
	def crear_carpeta(self, usuario, ruta: str):
		"""
		Crea una carpeta o estructura de carpetas para un usuario.
		
		Args:
			usuario: Instancia de Usuario
			ruta: Ruta de la carpeta (ej: "Trabajo/Proyectos/2025")
		
		Complejidad: O(d) donde d es la profundidad de la ruta
		"""
		return usuario.obtener_o_crear_carpeta(ruta)
	
	def listar_carpetas(self, usuario) -> List[str]:
		"""
		Lista todas las carpetas de un usuario de forma recursiva.
		
		Complejidad: O(c) donde c es el número total de carpetas
		"""
		return usuario.listar_carpetas()
	
	def obtener_estadisticas_carpeta(self, carpeta) -> dict:
		"""
		Obtiene estadísticas de una carpeta.
		
		Returns:
			Diccionario con cantidad de mensajes y subcarpetas
		
		Complejidad: O(1) para mensajes directos, O(n) para recursivo
		"""
		mensajes_directos = len(carpeta.listar_mensajes())
		subcarpetas = len(carpeta.listar_subcarpetas())
		
		# Conteo recursivo de todos los mensajes
		total_mensajes = mensajes_directos
		for subcarpeta in carpeta.listar_subcarpetas().values():
			total_mensajes += self._contar_mensajes_recursivo(subcarpeta)
		
		return {
			"mensajes_directos": mensajes_directos,
			"mensajes_totales": total_mensajes,
			"subcarpetas_directas": subcarpetas,
		}
	
	def _contar_mensajes_recursivo(self, carpeta) -> int:
		"""Cuenta mensajes en una carpeta y todas sus subcarpetas."""
		total = len(carpeta.listar_mensajes())
		for subcarpeta in carpeta.listar_subcarpetas().values():
			total += self._contar_mensajes_recursivo(subcarpeta)
		return total
	
	def recorrer_estructura(self, usuario) -> List[Tuple[str, object]]:
		"""
		Recorre la estructura completa de carpetas de un usuario.
		
		Returns:
			Lista de tuplas (ruta, carpeta)
		
		Complejidad: O(c) donde c es el número de carpetas
		"""
		return list(usuario.recorrer_carpetas())
