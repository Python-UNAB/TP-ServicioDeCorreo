from __future__ import annotations

from collections import deque
from typing import Deque, Iterator, TYPE_CHECKING

if TYPE_CHECKING:
	from ..models.carpeta import Carpeta


def dfs_carpeta(raiz: "Carpeta") -> Iterator["Carpeta"]:
	"""Genera carpetas en recorrido en profundidad (DFS)."""
	yield raiz
	for subcarpeta in raiz.listar_subcarpetas().values():
		yield from dfs_carpeta(subcarpeta)


def bfs_carpeta(raiz: "Carpeta") -> Iterator["Carpeta"]:
	"""Genera carpetas en recorrido en amplitud (BFS)."""
	cola: Deque["Carpeta"] = deque([raiz])
	while cola:
		carpeta = cola.popleft()
		yield carpeta
		cola.extend(carpeta.listar_subcarpetas().values())
