"""Algoritmos de búsqueda recursiva en la estructura de carpetas.

Complejidad temporal: O(n) donde n es el número total de mensajes
en todas las carpetas y subcarpetas.
"""
from typing import Callable, List


def buscar_en_carpetas(carpeta, criterio: Callable) -> List:
	"""
	Realiza una búsqueda recursiva en una carpeta y todas sus subcarpetas.
	
	Args:
		carpeta: Instancia de Carpeta desde donde iniciar la búsqueda
		criterio: Función que recibe un mensaje y retorna True si cumple la condición
	
	Returns:
		Lista de mensajes que cumplen el criterio
	
	Complejidad: O(n) donde n es el total de mensajes en el árbol de carpetas
	"""
	return carpeta.buscar_mensajes(criterio)


def buscar_por_remitente(carpeta, remitente: str) -> List:
	"""
	Busca todos los mensajes de un remitente específico.
	
	Args:
		carpeta: Carpeta raíz desde donde buscar
		remitente: Nombre de usuario del remitente
	
	Returns:
		Lista de mensajes del remitente
	
	Complejidad: O(n) donde n es el total de mensajes
	"""
	return buscar_en_carpetas(
		carpeta,
		lambda mensaje: mensaje.mostrar_remitente == remitente
	)


def buscar_por_asunto(carpeta, texto: str) -> List:
	"""
	Busca mensajes que contengan el texto en el asunto.
	
	Args:
		carpeta: Carpeta raíz desde donde buscar
		texto: Texto a buscar en el asunto (case-insensitive)
	
	Returns:
		Lista de mensajes que contienen el texto
	
	Complejidad: O(n*m) donde n es total de mensajes y m el largo del asunto
	"""
	texto_lower = texto.lower()
	return buscar_en_carpetas(
		carpeta,
		lambda mensaje: texto_lower in mensaje.mostrar_asunto.lower()
	)
