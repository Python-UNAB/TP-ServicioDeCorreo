"""Algoritmos de recorrido de grafos (BFS y DFS) para carpetas.

Estos algoritmos son útiles para explorar la estructura jerárquica de carpetas
y pueden extenderse para modelar redes de servidores de correo.
"""
from collections import deque
from typing import List, Tuple


def recorrer_carpetas_bfs(carpeta_raiz) -> List[Tuple[str, object]]:
	"""
	Recorrido en anchura (BFS) de la estructura de carpetas.
	
	Args:
		carpeta_raiz: Carpeta desde donde iniciar el recorrido
	
	Returns:
		Lista de tuplas (ruta, carpeta) en orden BFS
	
	Complejidad: O(n) donde n es el número total de carpetas
	Espacio: O(w) donde w es el ancho máximo del árbol
	"""
	resultado = []
	cola = deque([(carpeta_raiz.nombre, carpeta_raiz)])
	
	while cola:
		ruta, carpeta = cola.popleft()
		resultado.append((ruta, carpeta))
		
		# Agregar subcarpetas a la cola
		for nombre, subcarpeta in sorted(carpeta.listar_subcarpetas().items()):
			nueva_ruta = f"{ruta}/{nombre}"
			cola.append((nueva_ruta, subcarpeta))
	
	return resultado


def recorrer_carpetas_dfs(carpeta_raiz) -> List[Tuple[str, object]]:
	"""
	Recorrido en profundidad (DFS) de la estructura de carpetas.
	
	Args:
		carpeta_raiz: Carpeta desde donde iniciar el recorrido
	
	Returns:
		Lista de tuplas (ruta, carpeta) en orden DFS
	
	Complejidad: O(n) donde n es el número total de carpetas
	Espacio: O(h) donde h es la altura del árbol (recursión)
	"""
	resultado = []
	
	def _dfs_recursivo(ruta: str, carpeta):
		resultado.append((ruta, carpeta))
		for nombre, subcarpeta in sorted(carpeta.listar_subcarpetas().items()):
			nueva_ruta = f"{ruta}/{nombre}"
			_dfs_recursivo(nueva_ruta, subcarpeta)
	
	_dfs_recursivo(carpeta_raiz.nombre, carpeta_raiz)
	return resultado


def recorrer_carpetas_dfs_iterativo(carpeta_raiz) -> List[Tuple[str, object]]:
	"""
	Versión iterativa del DFS usando una pila explícita.
	
	Args:
		carpeta_raiz: Carpeta desde donde iniciar el recorrido
	
	Returns:
		Lista de tuplas (ruta, carpeta) en orden DFS
	
	Complejidad: O(n)
	Espacio: O(h) donde h es la altura del árbol
	"""
	resultado = []
	pila = [(carpeta_raiz.nombre, carpeta_raiz)]
	
	while pila:
		ruta, carpeta = pila.pop()
		resultado.append((ruta, carpeta))
		
		# Agregar subcarpetas a la pila (en orden inverso para mantener orden alfabético)
		for nombre, subcarpeta in sorted(carpeta.listar_subcarpetas().items(), reverse=True):
			nueva_ruta = f"{ruta}/{nombre}"
			pila.append((nueva_ruta, subcarpeta))
	
	return resultado
