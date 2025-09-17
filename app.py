
import datetime

class Usuario:
	def __init__(self, username: str, password: str):
		"""Creamos el constructor de la clase Usuario con 2 parámetros, username y password que serán usados para autenticar"""
		self.__username = username
		self.__password = password
		self.__carpetas = {
            "Entrada": Carpeta("Entrada"),
            "Enviados": Carpeta("Enviados")
        }

	@property
	def username(self):
		return self.__username
	@property
	def password(self):
		return self.__password
	
	def obtener_carpeta(self, nombre):
		return self.__carpetas.get(nombre)
    
	def listar_carpetas(self):
		return list(self.__carpetas.keys())


class Mensaje:
	def __init__(self, remitente: str, destinatario: str, asunto: str, cuerpo: str):
		"""La clase mensaje representa a todo mensaje que envía o recibe un usuario"""
		self.__remitente = remitente
		self.__destinatario = destinatario
		self.__asunto = asunto
		self.__cuerpo = cuerpo
		self.__fecha = datetime.now()         # Fecha automática

	@property
	def mostrar_remitente(self):
		return self.__remitente
	@property
	def mostrar_destinatario(self):
		return self.__destinatario
	@property
	def mostrar_asunto(self):
		return self.__asunto
	@property
	def mostrar_cuerpo(self):
		return self.__cuerpo
	
	def mostrar_correo(self):
		return (f"De: {self.__remitente}\n"
        		f"Para: {self.__destinatario}\n"
                f"Asunto: {self.__asunto}\n"
                f"Contenido: {self.__cuerpo}")
	
	def mostrar_resumen(self):
		return f"{self.__fecha.strftime('%Y-%m-%d %H:%M')} - {self.__asunto} (de {self.__remitente})"

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
		if destinatario not in self.__usuarios:
			return f'El usuario {destinatario} no existe'
		msg = Mensaje(remitente, destinatario, asunto, cuerpo)
		# Se guarda en "Enviados" del remitente 
		self.__usuarios[remitente].obtener_carpeta("Enviados").agregar_mensaje(msg)
    	# Se guarda en "Entrada" del destinatario
		self.__usuarios[destinatario].obtener_carpeta("Entrada").agregar_mensaje(msg)
		return True

class Carpeta:
    def __init__(self, nombre_carpeta):
        self.__nombre_carpeta = nombre_carpeta
        self.__mensajes = []   # lista de Mensajes (objeto)
    
    @property
    def nombre(self):
        return self.__nombre_carpeta

    def agregar_mensaje(self, mensaje):
        self.__mensajes.append(mensaje)

    def listar_mensajes(self):
        return [m.mostrar_resumen() for m in self.__mensajes]
	
def menu_servidor():
	server = ServidorCorreo()
	2
	try:
		server.registrar_usuario("MikeMz", "1234")
	except ValueError:
		pass
	while True:
		print("\n--- MENÚ SERVIDOR DE CORREO ---")
		print("1. Ingresar")
		print("2. Registrarse")
		print("3. Salir")
		opcion = input("Seleccione una opción: ")

		if opcion == "1":
			username = input("Usuario: ")
			password = input("Contraseña: ")
			usuario = server.autenticar(username, password)
			if usuario:
				print(f"Bienvenido, {username}!")
				#Acá iría el menu de inicio del usuario autenticado
			else:
				print("Usuario o contraseña incorrectos.")
		elif opcion == "2":
			username = input("Nuevo usuario: ")
			password = input("Nueva contraseña: ")
			try:
				print(server.registrar_usuario(username, password))
			except ValueError as e:
				print(e)
		elif opcion == "3":
			print("¡Hasta luego!")
			break
		else:
			print("Opción inválida.")

if __name__ == "__main__":
    menu_servidor()
