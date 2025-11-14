"""Gestión de red de servidores (preparado para futuras extensiones)."""
from typing import Dict, List, Optional


class GestorRed:
	"""
	Clase preparada para gestionar una red de servidores de correo.
	
	Esta clase es una base para implementar:
	- Comunicación entre múltiples servidores
	- Enrutamiento de mensajes entre dominios
	- Sincronización de usuarios
	"""
	
	def __init__(self):
		self.servidores: Dict[str, object] = {}  # dominio -> ServidorCorreo
		self.grafo_conexiones: Dict[str, List[str]] = {}  # Grafo de conexiones entre servidores
	
	def registrar_servidor(self, dominio: str, servidor):
		"""
		Registra un servidor en la red.
		
		Args:
			dominio: Nombre del dominio (ej: "example.com")
			servidor: Instancia de ServidorCorreo
		"""
		if dominio in self.servidores:
			raise ValueError(f"El dominio {dominio} ya está registrado")
		self.servidores[dominio] = servidor
		self.grafo_conexiones[dominio] = []
	
	def conectar_servidores(self, dominio1: str, dominio2: str):
		"""
		Establece una conexión bidireccional entre dos servidores.
		
		Complejidad: O(1)
		"""
		if dominio1 not in self.servidores or dominio2 not in self.servidores:
			raise ValueError("Uno o ambos dominios no existen")
		
		if dominio2 not in self.grafo_conexiones[dominio1]:
			self.grafo_conexiones[dominio1].append(dominio2)
		if dominio1 not in self.grafo_conexiones[dominio2]:
			self.grafo_conexiones[dominio2].append(dominio1)
	
	def encontrar_ruta(self, origen: str, destino: str) -> Optional[List[str]]:
		"""
		Encuentra una ruta entre dos servidores usando BFS.
		
		Args:
			origen: Dominio de origen
			destino: Dominio de destino
		
		Returns:
			Lista de dominios que forman la ruta, o None si no existe
		
		Complejidad: O(V + E) donde V es servidores y E conexiones
		"""
		if origen not in self.servidores or destino not in self.servidores:
			return None
		
		if origen == destino:
			return [origen]
		
		from collections import deque
		
		cola = deque([(origen, [origen])])
		visitados = {origen}
		
		while cola:
			actual, ruta = cola.popleft()
			
			for vecino in self.grafo_conexiones.get(actual, []):
				if vecino == destino:
					return ruta + [vecino]
				
				if vecino not in visitados:
					visitados.add(vecino)
					cola.append((vecino, ruta + [vecino]))
		
		return None  # No existe ruta
	
	def obtener_servidor(self, dominio: str):
		"""Obtiene el servidor de un dominio específico."""
		return self.servidores.get(dominio)
	
	def listar_dominios(self) -> List[str]:
		"""Lista todos los dominios registrados."""
		return list(self.servidores.keys())
