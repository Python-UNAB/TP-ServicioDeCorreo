from .servidor import ServidorCorreo



def menu_usuario(servidor: ServidorCorreo, usuario):
    print(f"\nSesión: {usuario.username}")
    while True:
        print("\n--- MENÚ USUARIO ---")
        print("1. Enviar mensaje")
        print("2. Ver Entrada")
        print("3. Ver Enviados")
        print("4. Cerrar sesión")
        op = input("Opción: ").strip()
        if op == "1":
            destinatario = input("Destinatario (username): ").strip()
            asunto = input("Asunto: ").strip()
            cuerpo = input("Contenido: ").strip()
            try:
                servidor.enviar_mensaje(usuario.username, destinatario, asunto, cuerpo)
                print("Mensaje enviado.")
            except ValueError as e:
                print(f"Error: {e}")
        elif op == "2":
            mensajes = usuario.obtener_carpeta("Entrada").listar_mensajes()
            if not mensajes:
                print("Entrada vacía.")
            for i, m in enumerate(mensajes, 1):
                print(f"{i}. {m.mostrar_resumen()}")
        elif op == "3":
            mensajes = usuario.obtener_carpeta("Enviados").listar_mensajes()
            if not mensajes:
                print("Enviados vacío.")
            for i, m in enumerate(mensajes, 1):
                print(f"{i}. {m.mostrar_resumen()}")
        elif op == "4":
            print("Sesión cerrada.")
            break
        else:
            print("Opción inválida.")

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
                menu_usuario(servidor, usuario)
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