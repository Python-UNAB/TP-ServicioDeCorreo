"""Algoritmos de ordenamiento de mensajes.

Se utilizan los algoritmos de ordenamiento nativos de Python (Timsort)
con complejidad O(n log n) en el caso promedio.
"""
from typing import List


def ordenar_por_fecha(mensajes: List, descendente: bool = True) -> List:
	"""
	Ordena mensajes por fecha.
	
	Args:
		mensajes: Lista de mensajes a ordenar
		descendente: Si True, ordena de más reciente a más antiguo
	
	Returns:
		Lista ordenada de mensajes
	
	Complejidad: O(n log n) usando Timsort
	"""
	return sorted(mensajes, key=lambda m: m.fecha, reverse=descendente)


def ordenar_por_prioridad(mensajes: List, descendente: bool = True) -> List:
	"""
	Ordena mensajes por prioridad (0 es máxima prioridad).
	
	Args:
		mensajes: Lista de mensajes a ordenar
		descendente: Si True, ordena de mayor a menor prioridad (0 primero)
	
	Returns:
		Lista ordenada de mensajes
	
	Complejidad: O(n log n)
	"""
	return sorted(mensajes, key=lambda m: m.prioridad, reverse=not descendente)


def ordenar_por_remitente(mensajes: List, ascendente: bool = True) -> List:
	"""
	Ordena mensajes alfabéticamente por nombre del remitente.
	
	Args:
		mensajes: Lista de mensajes a ordenar
		ascendente: Si True, ordena de A a Z
	
	Returns:
		Lista ordenada de mensajes
	
	Complejidad: O(n log n)
	"""
	return sorted(mensajes, key=lambda m: m.mostrar_remitente, reverse=not ascendente)
