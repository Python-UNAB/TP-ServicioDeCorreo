from .usuario import Usuario
from .mensaje import Mensaje


class ServidorCorreo:
	"""El servidor principal. Permite registrar usuarios simulando una base de datos y los guarda en una lista, para poder autenticarse"""
	def __init__(self):
		self.__usuarios = {} #Diccionario con Usuarios (objeto) registrados

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
	
	def mostrar_usuarios_registrados(self):
		return self.__usuarios.keys()

	def enviar_mensaje(self, remitente, destinatario, asunto, cuerpo):
		if remitente not in self.__usuarios:
			raise ValueError("El remitente no existe.")
		if destinatario not in self.__usuarios:
			raise ValueError("El destinatario no existe.")
		rem = self.__usuarios[remitente]
		dest = self.__usuarios[destinatario]
		mensaje = Mensaje(rem, dest, asunto, cuerpo)
		rem.obtener_carpeta("Enviados").agregar_mensaje(mensaje)
		dest.obtener_carpeta("Entrada").agregar_mensaje(mensaje)