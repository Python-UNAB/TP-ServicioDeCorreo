from .servidor import ServidorCorreo


def seleccionar_carpeta(usuario):
    rutas = usuario.listar_carpetas()
    if not rutas:
        print("No hay carpetas disponibles.")
        return None
    for idx, ruta in enumerate(rutas, 1):
        print(f"{idx}. {ruta}")
    try:
        seleccion = int(input("Seleccione carpeta: "))
        if 1 <= seleccion <= len(rutas):
            return rutas[seleccion - 1]
    except ValueError:
        pass
    print("Selección inválida.")
    return None


def mostrar_mensajes_de_carpeta(usuario, ruta):
    carpeta = usuario.obtener_carpeta(ruta)
    if carpeta is None:
        print("La carpeta no existe.")
        return
    mensajes = carpeta.listar_mensajes()
    if not mensajes:
        print("La carpeta está vacía.")
        return
    for idx, mensaje in enumerate(mensajes, 1):
        print(f"{idx}. {mensaje.mostrar_resumen()}")


def menu_usuario(servidor: ServidorCorreo, usuario):
    print(f"\nSesión: {usuario.username}")
    while True:
        print("\n--- MENÚ USUARIO ---")
        print("1. Enviar mensaje")
        print("2. Ver mensajes de una carpeta")
        print("3. Buscar mensajes por texto")
        print("4. Mover mensajes")
        print("5. Crear carpeta")
        print("6. Agregar filtro por asunto")
        print("7. Listar filtros activos")
        print("8. Cerrar sesión")
        op = input("Opción: ").strip()
        if op == "1":
            destinatario = input("Destinatario (username): ").strip()
            asunto = input("Asunto: ").strip()
            cuerpo = input("Contenido: ").strip()
            urgente_input = input("¿Marcar como urgente? (s/n): ").strip().lower()
            urgente = urgente_input in {"s", "si", "y"}
            prioridad = 0
            if urgente:
                try:
                    prioridad = int(input("Prioridad (0 es la más alta, por defecto 0): ") or "0")
                except ValueError:
                    prioridad = 0
            try:
                servidor.enviar_mensaje(usuario.username, destinatario, asunto, cuerpo, urgente=urgente, prioridad=prioridad)
                print("Mensaje enviado.")
            except ValueError as e:
                print(f"Error: {e}")
        elif op == "2":
            ruta = seleccionar_carpeta(usuario)
            if ruta:
                mostrar_mensajes_de_carpeta(usuario, ruta)
        elif op == "3":
            texto = input("Texto a buscar: ").strip().lower()
            if not texto:
                print("Debe ingresar un texto.")
                continue
            resultados = usuario.buscar_mensajes(lambda mensaje: texto in mensaje.mostrar_asunto.lower() or texto in mensaje.mostrar_cuerpo.lower())
            if not resultados:
                print("Sin coincidencias.")
                continue
            for idx, mensaje in enumerate(resultados, 1):
                print(f"{idx}. {mensaje.mostrar_resumen()}")
        elif op == "4":
            texto = input("Texto que identifica los mensajes a mover: ").strip().lower()
            destino = input("Carpeta destino (use / para subcarpetas): ").strip()
            if not texto or not destino:
                print("Texto y destino son obligatorios.")
                continue
            origen = input("Carpeta origen (Enter para buscar en todas): ").strip() or None
            crear_dest = input("¿Crear carpeta destino si no existe? (s/n): ").strip().lower() in {"s", "si", "y"}
            try:
                movidos = usuario.mover_mensajes(lambda mensaje: texto in mensaje.mostrar_asunto.lower() or texto in mensaje.mostrar_cuerpo.lower(), destino, origen_ruta=origen, crear_destino=crear_dest)
                print(f"Se movieron {movidos} mensajes.")
            except (ValueError, LookupError) as e:
                print(f"Error: {e}")
        elif op == "5":
            ruta = input("Nombre completo de la nueva carpeta (Ej: Entrada/Proyectos): ").strip()
            if not ruta:
                print("La ruta no puede estar vacía.")
                continue
            try:
                usuario.obtener_o_crear_carpeta(ruta)
                print(f"Carpeta '{ruta}' disponible.")
            except ValueError as e:
                print(f"Error: {e}")
        elif op == "6":
            nombre = input("Nombre del filtro: ").strip()
            palabra = input("Palabra clave en el asunto: ").strip().lower()
            destino = input("Carpeta destino: ").strip()
            crear_dest = input("¿Crear carpeta destino si no existe? (s/n): ").strip().lower() in {"s", "si", "y"}
            if not nombre or not palabra or not destino:
                print("Todos los campos son obligatorios.")
                continue
            try:
                usuario.agregar_filtro(nombre, lambda mensaje, palabra=palabra: palabra in mensaje.mostrar_asunto.lower(), destino, crear_destino=crear_dest)
                print("Filtro agregado.")
            except ValueError as e:
                print(f"Error: {e}")
        elif op == "7":
            filtros = usuario.listar_filtros()
            if not filtros:
                print("No hay filtros activos.")
            else:
                print("Filtros activos:")
                for nombre in filtros:
                    print(f"- {nombre}")
        elif op == "8":
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
        print("3. Atender mensaje urgente")
        print("4. Salir")
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
            mensaje = servidor.extraer_mensaje_urgente()
            if mensaje is None:
                print("No hay mensajes urgentes en espera.")
            else:
                print("Mensaje urgente atendido:")
                print(mensaje.mostrar_correo())
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_servidor()