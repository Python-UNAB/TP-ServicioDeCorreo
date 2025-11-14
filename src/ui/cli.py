"""Interfaz de línea de comandos principal."""
from ..models import ServidorCorreo
from .menu import MenuPrincipal, MenuUsuario


def ejecutar_cli():
	"""Punto de entrada principal de la aplicación CLI."""
	servidor = ServidorCorreo()
	
	# Crear usuario de prueba
	try:
		servidor.registrar_usuario("MikeMz", "1234")
	except ValueError:
		pass
	
	menu_principal = MenuPrincipal(servidor)
	
	while True:
		menu_principal.mostrar()
		opcion = input("Seleccione una opción: ")
		
		continuar, usuario = menu_principal.procesar_opcion(opcion)
		
		if not continuar:
			break
		
		if usuario:
			ejecutar_menu_usuario(servidor, usuario)


def ejecutar_menu_usuario(servidor, usuario):
	"""Ejecuta el menú de usuario autenticado."""
	menu_usuario = MenuUsuario(servidor, usuario)
	
	while True:
		menu_usuario.mostrar()
		op = input("Opción: ").strip()
		
		if not menu_usuario.procesar_opcion(op):
			break
