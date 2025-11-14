"""Gestión de operaciones con mensajes."""
from typing import List, Optional


class GestorMensajes:
	"""Clase para gestionar operaciones sobre mensajes."""
	
	def __init__(self, servidor):
		"""
		Args:
			servidor: Instancia de ServidorCorreo
		"""
		self.servidor = servidor
	
	def enviar(self, remitente: str, destinatario: str, asunto: str, cuerpo: str, 
	           urgente: bool = False, prioridad: int = 0):
		"""
		Envía un mensaje entre usuarios.
		
		Complejidad: O(f) donde f es el número de filtros del destinatario
		"""
		return self.servidor.enviar_mensaje(
			remitente, destinatario, asunto, cuerpo,
			urgente=urgente, prioridad=prioridad
		)
	
	def buscar_mensajes_usuario(self, username: str, criterio, carpeta_ruta: Optional[str] = None) -> List:
		"""
		Busca mensajes de un usuario según un criterio.
		
		Complejidad: O(n) donde n es el número de mensajes del usuario
		"""
		usuario = self.servidor.obtener_usuario(username)
		if usuario is None:
			raise ValueError(f"Usuario {username} no existe")
		return usuario.buscar_mensajes(criterio, carpeta_ruta)
	
	def mover_mensajes_usuario(self, username: str, criterio, destino_ruta: str, 
	                           origen_ruta: Optional[str] = None, crear_destino: bool = False) -> int:
		"""
		Mueve mensajes de un usuario según criterio.
		
		Complejidad: O(n) donde n es el número de mensajes a revisar
		"""
		usuario = self.servidor.obtener_usuario(username)
		if usuario is None:
			raise ValueError(f"Usuario {username} no existe")
		return usuario.mover_mensajes(criterio, destino_ruta, origen_ruta, crear_destino=crear_destino)
	
	def obtener_mensajes_urgentes(self) -> List:
		"""
		Obtiene todos los mensajes urgentes pendientes.
		
		Returns:
			Lista de mensajes urgentes en orden de prioridad
		"""
		urgentes = []
		while self.servidor.tiene_mensajes_urgentes():
			mensaje = self.servidor.extraer_mensaje_urgente()
			if mensaje:
				urgentes.append(mensaje)
		return urgentes
