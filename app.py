

class Usuario:
	def __init__(self, username: str, password: str):
		self.__username = username
		self.__password = password

class Mensaje:
	def __init__(self, remitente: str, destinatario: str, asunto: str, cuerpo: str):
		self.__remitente = remitente
		self.__destinatario = destinatario
		self.__asunto = asunto
		self.__cuerpo = cuerpo

class ServidorCorreo:
	def __init__(self):
		self.__usuarios = {} #Diccionario con Usuarios registrados

	def registrar_usuarios(self, username, password):
		if username in self.__usuarios:
			raise ValueError(f'El usuario {username} ya se encuentra registrado')
		self.__usuarios[username] = Usuario(username, password)
        


