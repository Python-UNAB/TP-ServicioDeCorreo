from .servidor import ServidorCorreo


def menu_servidor():
	servidor = ServidorCorreo()
	try:
		servidor.registrar_usuario("MikeMz", "1234")
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
			usuario = servidor.autenticar(username, password)
			if usuario:
				print(f"Bienvenido, {username}!")
				# Acá iría el menú de usuario autenticado (enviar/ver mensajes)
			else:
				print("Usuario o contraseña incorrectos.")
		elif opcion == "2":
			username = input("Nuevo usuario: ")
			password = input("Nueva contraseña: ")
			try:
				print(servidor.registrar_usuario(username, password))
			except ValueError as e:
				print(e)
		elif opcion == "3":
			print("¡Hasta luego!")
			break
		else:
			print("Opción inválida.")

if __name__ == "__main__":
    menu_servidor()
