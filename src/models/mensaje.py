from __future__ import annotations
from datetime import datetime
from typing import Optional


class Mensaje:
	def __init__(self, remitente, destinatario, asunto: str, cuerpo: str, *, urgente: bool = False, prioridad: Optional[int] = None):
		"""Representa un mensaje entre usuarios del sistema.

		remitente: Usuario
		destinatario: Usuario
		"""
		self.__remitente = remitente
		self.__destinatario = destinatario
		self.__asunto = asunto
		self.__cuerpo = cuerpo
		self.__fecha = datetime.now()
		self.__prioridad = self._resolver_prioridad(prioridad, urgente)
		self.__urgente = self.__prioridad is not None

	def _resolver_prioridad(self, prioridad: Optional[int], urgente: bool) -> Optional[int]:
		if prioridad is not None:
			if not 1 <= prioridad <= 5:
				raise ValueError("La prioridad debe estar entre 1 y 5")
			return prioridad
		if urgente:
			return 1
		return None

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

	@property
	def prioridad(self) -> Optional[int]:
		return self.__prioridad
	
	def mostrar_correo(self):
		lineas = [
			f"De: {self.mostrar_remitente}",
			f"Para: {self.mostrar_destinatario}",
			f"Asunto: {self.__asunto}",
			f"Contenido: {self.__cuerpo}",
		]
		if self.__prioridad is not None:
			lineas.append(f"Prioridad: {self.__prioridad}")
		return "\n".join(lineas)
	
	def mostrar_resumen(self):
		prefijo = "[URGENTE] " if self.__urgente else ""
		sufijo = ""
		if self.__prioridad is not None:
			sufijo = f" [P={self.__prioridad}]"
		return f"{prefijo}{self.__fecha.strftime('%Y-%m-%d %H:%M')} - {self.__asunto} (de {self.mostrar_remitente}){sufijo}"
