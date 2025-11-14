"""Algoritmos de búsqueda, ordenamiento y recorrido."""
from .busqueda_recursiva import buscar_en_carpetas, buscar_por_remitente, buscar_por_asunto
from .ordenamiento import ordenar_por_fecha, ordenar_por_prioridad, ordenar_por_remitente
from .recorrido_grafo import recorrer_carpetas_bfs, recorrer_carpetas_dfs

__all__ = [
    'buscar_en_carpetas',
    'buscar_por_remitente',
    'buscar_por_asunto',
    'ordenar_por_fecha',
    'ordenar_por_prioridad',
    'ordenar_por_remitente',
    'recorrer_carpetas_bfs',
    'recorrer_carpetas_dfs',
]
