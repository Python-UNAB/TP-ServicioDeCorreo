from __future__ import annotations

from typing import Callable


class Filtro:
	"""Regla de clasificación automática para mensajes entrantes."""

	def __init__(self, nombre: str, condicion: Callable, destino_ruta: str, *, crear_destino: bool = True):
		self._nombre = nombre
		self._condicion = condicion
		self._destino_ruta = destino_ruta
		self._crear_destino = crear_destino

	@property
	def nombre(self) -> str:
		return self._nombre

	@property
	def destino_ruta(self) -> str:
		return self._destino_ruta

	@property
	def crear_destino(self) -> bool:
		return self._crear_destino

	def aplica_a(self, mensaje) -> bool:
		"""Evalúa si el mensaje cumple la condición del filtro."""
		return self._condicion(mensaje)
