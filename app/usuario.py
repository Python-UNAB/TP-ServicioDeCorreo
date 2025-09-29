from .carpeta import Carpeta


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