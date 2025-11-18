from __future__ import annotations

from typing import Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
	from ..models.carpeta import Carpeta
	from ..models.mensaje import Mensaje


FiltroMensaje = Callable[["Mensaje"], bool]


def buscar_mensajes_en_carpeta(carpeta: "Carpeta", criterio: FiltroMensaje) -> List["Mensaje"]:
	"""Devuelve los mensajes que cumplen el criterio recorriendo recursivamente."""
	resultado = [mensaje for mensaje in carpeta.listar_mensajes() if criterio(mensaje)]
	for subcarpeta in carpeta.listar_subcarpetas().values():
		resultado.extend(buscar_mensajes_en_carpeta(subcarpeta, criterio))
	return resultado
	


def extraer_mensajes_en_carpeta(carpeta: "Carpeta", criterio: FiltroMensaje) -> List["Mensaje"]:
	"""Extrae mensajes que cumplen el criterio, eliminándolos de cada carpeta visitada."""
	extraidos: List["Mensaje"] = []
	for mensaje in list(carpeta.listar_mensajes()):
		if criterio(mensaje) and carpeta.eliminar_mensaje(mensaje):
			extraidos.append(mensaje)
	for subcarpeta in carpeta.listar_subcarpetas().values():
		extraidos.extend(extraer_mensajes_en_carpeta(subcarpeta, criterio))
	return extraidos
