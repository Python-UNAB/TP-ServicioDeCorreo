import heapq
from itertools import count
from typing import Optional

from ..models.usuario import Usuario
from ..models.mensaje import Mensaje


class ServidorCorreo:
	"""Servidor principal que gestiona usuarios y enruta mensajes."""
	def __init__(self):
		self.__usuarios = {}  # Diccionario: username -> Usuario
		self.__cola_urgentes = []  # Heap de mensajes urgentes (prioridad, orden, mensaje)
		self.__contador_prioridad = count()  # Rompe empates manteniendo orden de llegada

	def registrar_usuario(self, username, password):
		if username in self.__usuarios:
			raise ValueError(f'El usuario {username} ya se encuentra registrado')
		self.__usuarios[username] = Usuario(username, password)
		return f'{username} registrado con éxito'
	
	def autenticar(self, username, password):
		usuario = self.__usuarios.get(username)
		if usuario and usuario.password == password:
			return usuario
		return None

	def obtener_usuario(self, username):
		return self.__usuarios.get(username)

	def enviar_mensaje(self, remitente, destinatario, asunto, cuerpo, *, urgente: bool = False, prioridad: Optional[int] = None):
		"""Envía un mensaje entre dos usuarios registrados.

		Si se indica `prioridad` (menor = más urgente) o `urgente=True`, el mensaje se encola en el heap de urgentes.
		"""
		if remitente not in self.__usuarios:
			raise ValueError("El remitente no existe.")
		if destinatario not in self.__usuarios:
			raise ValueError("El destinatario no existe.")
		rem = self.__usuarios[remitente]
		dest = self.__usuarios[destinatario]
		if prioridad is not None and not 1 <= prioridad <= 5:
			raise ValueError("La prioridad debe estar entre 1 y 5")
		prioridad_resuelta = prioridad if prioridad is not None else (1 if urgente else None)
		mensaje = Mensaje(rem, dest, asunto, cuerpo, urgente=urgente, prioridad=prioridad_resuelta)
		rem.obtener_carpeta("Enviados").agregar_mensaje(mensaje)
		entrada_dest = dest.obtener_carpeta("Entrada")
		if entrada_dest is None:
			dest.obtener_o_crear_carpeta("Entrada")
			entrada_dest = dest.obtener_carpeta("Entrada")
		entrada_dest.agregar_mensaje(mensaje)
		dest.aplicar_filtros(mensaje)
		prioridad_heap = mensaje.prioridad
		if prioridad_heap is not None:
			heapq.heappush(self.__cola_urgentes, (prioridad_heap, next(self.__contador_prioridad), mensaje))
		return mensaje

	def tiene_mensajes_urgentes(self) -> bool:
		"""Verifica si hay mensajes urgentes pendientes."""
		return bool(self.__cola_urgentes)

	def extraer_mensaje_urgente(self):
		"""Extrae el mensaje urgente más antiguo (FIFO)."""
		if not self.__cola_urgentes:
			return None
		return heapq.heappop(self.__cola_urgentes)[2]
