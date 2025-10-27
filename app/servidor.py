import heapq
from itertools import count

from .usuario import Usuario
from .mensaje import Mensaje


class ServidorCorreo:
	"""El servidor principal. Permite registrar usuarios simulando una base de datos y los guarda en una lista, para poder autenticarse"""
	def __init__(self):
		self.__usuarios = {} #Diccionario con Usuarios (objeto) registrados
		self.__cola_urgentes = []
		self.__contador_urgentes = count()

	def registrar_usuario(self, username, password):
		if username in self.__usuarios:
			raise ValueError(f'El usuario {username} ya se encuentra registrado')
		self.__usuarios[username] = Usuario(username, password)
		return f'{username} registrado con éxito'
	
	def autenticar(self, username, password):
		usuario = self.__usuarios.get(username)
		if usuario and usuario.password == password:
			return usuario
		return None

	def obtener_usuario(self, username):
		return self.__usuarios.get(username)
	
	def mostrar_usuarios_registrados(self):
		return self.__usuarios.keys()

	def enviar_mensaje(self, remitente, destinatario, asunto, cuerpo, *, urgente: bool = False, prioridad: int = 0):
		if remitente not in self.__usuarios:
			raise ValueError("El remitente no existe.")
		if destinatario not in self.__usuarios:
			raise ValueError("El destinatario no existe.")
		rem = self.__usuarios[remitente]
		dest = self.__usuarios[destinatario]
		mensaje = Mensaje(rem, dest, asunto, cuerpo, urgente=urgente, prioridad=prioridad)
		rem.obtener_carpeta("Enviados").agregar_mensaje(mensaje)
		entrada_dest = dest.obtener_carpeta("Entrada")
		if entrada_dest is None:
			dest.obtener_o_crear_carpeta("Entrada")
			entrada_dest = dest.obtener_carpeta("Entrada")
		entrada_dest.agregar_mensaje(mensaje)
		dest.aplicar_filtros(mensaje)
		if urgente:
			heapq.heappush(self.__cola_urgentes, (prioridad, next(self.__contador_urgentes), mensaje))
		return mensaje

	def tiene_mensajes_urgentes(self) -> bool:
		return bool(self.__cola_urgentes)

	def extraer_mensaje_urgente(self):
		if not self.__cola_urgentes:
			return None
		_, _, mensaje = heapq.heappop(self.__cola_urgentes)
		return mensaje

	def registrar_filtro(self, username, nombre, condicion, destino_ruta, *, crear_destino=True):
		usuario = self.__usuarios.get(username)
		if usuario is None:
			raise ValueError("El usuario no existe")
		usuario.agregar_filtro(nombre, condicion, destino_ruta, crear_destino=crear_destino)