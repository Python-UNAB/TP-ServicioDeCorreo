from .usuario import Usuario
from .mensaje import Mensaje


class ServidorCorreo:
	"""Servidor principal que gestiona usuarios y enruta mensajes."""
	def __init__(self):
		self.__usuarios = {}  # Diccionario: username -> Usuario
		self.__cola_urgentes = []  # Cola FIFO de mensajes urgentes

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

	def enviar_mensaje(self, remitente, destinatario, asunto, cuerpo, *, urgente: bool = False):
		"""Envía un mensaje entre dos usuarios registrados."""
		if remitente not in self.__usuarios:
			raise ValueError("El remitente no existe.")
		if destinatario not in self.__usuarios:
			raise ValueError("El destinatario no existe.")
		rem = self.__usuarios[remitente]
		dest = self.__usuarios[destinatario]
		mensaje = Mensaje(rem, dest, asunto, cuerpo, urgente=urgente)
		# Guardar en carpeta "Enviados" del remitente
		rem.obtener_carpeta("Enviados").agregar_mensaje(mensaje)
		# Guardar en carpeta "Entrada" del destinatario
		entrada_dest = dest.obtener_carpeta("Entrada")
		if entrada_dest is None:
			dest.obtener_o_crear_carpeta("Entrada")
			entrada_dest = dest.obtener_carpeta("Entrada")
		entrada_dest.agregar_mensaje(mensaje)
		# Aplicar filtros automáticos del destinatario
		dest.aplicar_filtros(mensaje)
		# Si es urgente, agregar a la cola FIFO
		if urgente:
			self.__cola_urgentes.insert(0, mensaje)  # Inserta al inicio (más reciente)
		return mensaje

	def tiene_mensajes_urgentes(self) -> bool:
		"""Verifica si hay mensajes urgentes pendientes."""
		return bool(self.__cola_urgentes)

	def extraer_mensaje_urgente(self):
		"""Extrae el mensaje urgente más antiguo (FIFO)."""
		if not self.__cola_urgentes:
			return None
		return self.__cola_urgentes.pop()  # Extrae del final (el más viejo)