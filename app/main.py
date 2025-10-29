from .servidor import ServidorCorreo


def menu_usuario(servidor: ServidorCorreo, usuario):
    print(f"\nSesión: {usuario.username}")
    while True:
        print("\n--- MENÚ USUARIO ---")
        print("1. Enviar mensaje")
        print("2. Ver mensajes de Entrada")
        print("3. Ver mensajes de Enviados")
        print("4. Mover mensajes")
        print("5. Crear carpeta")
        print("6. Ver carpetas")
        print("7. Agregar filtro por asunto")
        print("8. Listar filtros activos")
        print("9. Ver mensajes urgentes")
        print("10. Cerrar sesión")
        op = input("Opción: ").strip()
        if op == "1":
            destinatario = input("Destinatario (username): ").strip()
            asunto = input("Asunto: ").strip()
            cuerpo = input("Contenido: ").strip()
            urgente_input = input("¿Marcar como urgente? (s/n): ").strip().lower()
            urgente = urgente_input in {"s", "si", "y"}
            try:
                servidor.enviar_mensaje(usuario.username, destinatario, asunto, cuerpo, urgente=urgente)
                print("Mensaje enviado.\n")
            except ValueError as e:
                print(f"Error: {e}\n")
        elif op == "2":
            mensajes = usuario.obtener_carpeta("Entrada").listar_mensajes()
            if not mensajes:
                print("Entrada vacía.\n")
                continue
            for i, m in enumerate(mensajes, 1):
                print(f"{i}. {m.mostrar_resumen()}")
            try:
                idx = int(input("Seleccioná número de mensaje (0 para volver): ").strip() or "0")
            except ValueError:
                print("Entrada inválida.\n")
                continue
            if idx == 0:
                continue
            if 1 <= idx <= len(mensajes):
                print("\n--- MENSAJE ---")
                print(mensajes[idx - 1].mostrar_correo())
                print()
            else:
                print("Índice fuera de rango.\n")
        elif op == "3":
            mensajes = usuario.obtener_carpeta("Enviados").listar_mensajes()
            if not mensajes:
                print("Enviados vacío.\n")
                continue
            for i, m in enumerate(mensajes, 1):
                print(f"{i}. {m.mostrar_resumen()}")
            try:
                idx = int(input("Seleccioná número de mensaje (0 para volver): ").strip() or "0")
            except ValueError:
                print("Entrada inválida.\n")
                continue
            if idx == 0:
                continue
            if 1 <= idx <= len(mensajes):
                print("\n--- MENSAJE ENVIADO ---")
                print(mensajes[idx - 1].mostrar_correo())
                print()
            else:
                print("Índice fuera de rango.\n")
        elif op == "4":
            texto = input("Texto que identifica los mensajes a mover: ").strip().lower()
            destino = input("Carpeta destino (use / para subcarpetas): ").strip()
            if not texto or not destino:
                print("Texto y destino son obligatorios.\n")
                continue
            origen = input("Carpeta origen (Enter para buscar en todas): ").strip() or None
            crear_dest = input("¿Crear carpeta destino si no existe? (s/n): ").strip().lower() in {"s", "si", "y"}
            try:
                movidos = usuario.mover_mensajes(lambda mensaje: texto in mensaje.mostrar_asunto.lower() or texto in mensaje.mostrar_cuerpo.lower(), destino, origen_ruta=origen, crear_destino=crear_dest)
                print(f"Se movieron {movidos} mensajes.\n")
            except (ValueError, LookupError) as e:
                print(f"Error: {e}\n")
        elif op == "5":
            ruta = input("Nombre completo de la nueva carpeta (Ej: Entrada/Proyectos): ").strip()
            if not ruta:
                print("La ruta no puede estar vacía.\n")
                continue
            try:
                usuario.obtener_o_crear_carpeta(ruta)
                print(f"Carpeta '{ruta}' disponible.\n")
            except ValueError as e:
                print(f"Error: {e}\n")
        elif op == "6":
            carpetas = usuario.listar_carpetas()
            if not carpetas:
                print("No hay carpetas disponibles.\n")
            else:
                print("\n--- CARPETAS DISPONIBLES ---")
                for carpeta in carpetas:
                    print(f"  • {carpeta}")
                print()
        elif op == "7":
            nombre = input("Nombre del filtro: ").strip()
            palabra = input("Palabra clave en el asunto: ").strip().lower()
            destino = input("Carpeta destino: ").strip()
            crear_dest = input("¿Crear carpeta destino si no existe? (s/n): ").strip().lower() in {"s", "si", "y"}
            if not nombre or not palabra or not destino:
                print("Todos los campos son obligatorios.\n")
                continue
            try:
                usuario.agregar_filtro(nombre, lambda mensaje, palabra=palabra: palabra in mensaje.mostrar_asunto.lower(), destino, crear_destino=crear_dest)
                print("Filtro agregado.\n")
            except ValueError as e:
                print(f"Error: {e}\n")
        elif op == "8":
            filtros = usuario.listar_filtros()
            if not filtros:
                print("No hay filtros activos.\n")
            else:
                print("Filtros activos:")
                for nombre in filtros:
                    print(f"- {nombre}")
                print()
        elif op == "9":
            if not servidor.tiene_mensajes_urgentes():
                print("No hay mensajes urgentes en espera.\n")
            else:
                print("\n--- MENSAJES URGENTES ---")
                while servidor.tiene_mensajes_urgentes():
                    mensaje = servidor.extraer_mensaje_urgente()
                    if mensaje:
                        print(mensaje.mostrar_correo())
                        print()
        elif op == "10":
            print("Sesión cerrada.\n")
            break
        else:
            print("Opción inválida.\n")


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
                print(f"Bienvenido, {username}!\n")
                menu_usuario(servidor, usuario)
            else:
                print("Usuario o contraseña incorrectos.\n")
        elif opcion == "2":
            username = input("Nuevo usuario: ")
            password = input("Nueva contraseña: ")
            try:
                print(servidor.registrar_usuario(username, password))
                print()
            except ValueError as e:
                print(e)
                print()
        elif opcion == "3":
            print("¡Hasta luego!\n")
            break
        else:
            print("Opción inválida.\n")


if __name__ == "__main__":
    menu_servidor()