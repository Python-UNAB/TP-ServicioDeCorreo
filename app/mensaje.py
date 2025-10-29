from __future__ import annotations
from datetime import datetime


class Mensaje:
	def __init__(self, remitente, destinatario, asunto: str, cuerpo: str, *, urgente: bool = False):
		"""Representa un mensaje entre usuarios del sistema.
		
		remitente: Usuario
		destinatario: Usuario
		"""
		self.__remitente = remitente
		self.__destinatario = destinatario
		self.__asunto = asunto
		self.__cuerpo = cuerpo
		self.__fecha = datetime.now()
		self.__urgente = urgente

	@property
	def mostrar_remitente(self):
		return getattr(self.__remitente, "username", str(self.__remitente))
	@property
	def mostrar_destinatario(self):
		return getattr(self.__destinatario, "username", str(self.__destinatario))
	@property
	def mostrar_asunto(self):
		return self.__asunto
	@property
	def mostrar_cuerpo(self):
		return self.__cuerpo

	@property
	def fecha(self):
		return self.__fecha

	@property
	def es_urgente(self):
		return self.__urgente
	
	def mostrar_correo(self):
		return (
			f"De: {self.mostrar_remitente}\n"
			f"Para: {self.mostrar_destinatario}\n"
			f"Asunto: {self.__asunto}\n"
			f"Contenido: {self.__cuerpo}"
		)
	
	def mostrar_resumen(self):
		prefijo = "[URGENTE] " if self.__urgente else ""
		return f"{prefijo}{self.__fecha.strftime('%Y-%m-%d %H:%M')} - {self.__asunto} (de {self.mostrar_remitente})"