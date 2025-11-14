from __future__ import annotations

from typing import Iterable, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
	from ..models.mensaje import Mensaje


def ordenar_mensajes_por_fecha(mensajes: Iterable["Mensaje"], *, descendente: bool = True) -> List["Mensaje"]:
	"""Ordena mensajes por fecha de envío."""
	return sorted(mensajes, key=lambda mensaje: mensaje.fecha, reverse=descendente)


def ordenar_mensajes_por_prioridad(mensajes: Iterable["Mensaje"], *, descendente_fecha: bool = False) -> List["Mensaje"]:
	"""Ordena mensajes por prioridad (menor = mayor urgencia) y fecha como desempate."""
	def clave(mensaje: "Mensaje"):
		prioridad: Optional[int] = mensaje.prioridad
		return (
			prioridad is None,
			prioridad if prioridad is not None else 0,
			-mensaje.fecha.timestamp() if descendente_fecha else mensaje.fecha.timestamp(),
		)

	return sorted(mensajes, key=clave)
