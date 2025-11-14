"""Sistema de menús del sistema de correo."""


class MenuPrincipal:
	"""Menú principal del servidor de correo."""
	
	def __init__(self, servidor):
		self.servidor = servidor
	
	def mostrar(self):
		"""Muestra las opciones del menú principal."""
		print("\n--- MENÚ SERVIDOR DE CORREO ---")
		print("1. Ingresar")
		print("2. Registrarse")
		print("3. Atender mensaje urgente")
		print("4. Salir")
	
	def procesar_opcion(self, opcion: str):
		"""
		Procesa la opción seleccionada por el usuario.
		
		Returns:
			Tuple (continuar, usuario_autenticado)
		"""
		if opcion == "1":
			return self._opcion_ingresar()
		elif opcion == "2":
			return self._opcion_registrarse()
		elif opcion == "3":
			return self._opcion_atender_urgente()
		elif opcion == "4":
			print("¡Hasta luego!")
			return False, None
		else:
			print("Opción inválida.")
			return True, None
	
	def _opcion_ingresar(self):
		"""Maneja el inicio de sesión."""
		username = input("Usuario: ")
		password = input("Contraseña: ")
		usuario = self.servidor.autenticar(username, password)
		if usuario:
			print(f"Bienvenido, {username}!")
			return True, usuario
		else:
			print("Usuario o contraseña incorrectos.")
			return True, None
	
	def _opcion_registrarse(self):
		"""Maneja el registro de nuevos usuarios."""
		username = input("Nuevo usuario: ")
		password = input("Nueva contraseña: ")
		try:
			print(self.servidor.registrar_usuario(username, password))
		except ValueError as e:
			print(e)
		return True, None
	
	def _opcion_atender_urgente(self):
		"""Atiende el siguiente mensaje urgente en la cola."""
		mensaje = self.servidor.extraer_mensaje_urgente()
		if mensaje is None:
			print("No hay mensajes urgentes en espera.")
		else:
			print("Mensaje urgente atendido:")
			print(mensaje.mostrar_correo())
		return True, None


class MenuUsuario:
	"""Menú de usuario autenticado."""
	
	def __init__(self, servidor, usuario):
		self.servidor = servidor
		self.usuario = usuario
	
	def mostrar(self):
		"""Muestra las opciones del menú de usuario."""
		print(f"\nSesión: {self.usuario.username}")
		print("\n--- MENÚ USUARIO ---")
		print("1. Enviar mensaje")
		print("2. Ver mensajes de una carpeta")
		print("3. Buscar mensajes por texto")
		print("4. Mover mensajes")
		print("5. Crear carpeta")
		print("6. Agregar filtro por asunto")
		print("7. Listar filtros activos")
		print("8. Cerrar sesión")
	
	def procesar_opcion(self, opcion: str):
		"""
		Procesa la opción seleccionada.
		
		Returns:
			True si debe continuar, False para cerrar sesión
		"""
		if opcion == "1":
			self._opcion_enviar_mensaje()
		elif opcion == "2":
			self._opcion_ver_carpeta()
		elif opcion == "3":
			self._opcion_buscar_mensajes()
		elif opcion == "4":
			self._opcion_mover_mensajes()
		elif opcion == "5":
			self._opcion_crear_carpeta()
		elif opcion == "6":
			self._opcion_agregar_filtro()
		elif opcion == "7":
			self._opcion_listar_filtros()
		elif opcion == "8":
			print("Sesión cerrada.")
			return False
		else:
			print("Opción inválida.")
		return True
	
	def _opcion_enviar_mensaje(self):
		"""Enviar un nuevo mensaje."""
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
			self.servidor.enviar_mensaje(self.usuario.username, destinatario, asunto, cuerpo, 
			                             urgente=urgente, prioridad=prioridad)
			print("Mensaje enviado.")
		except ValueError as e:
			print(f"Error: {e}")
	
	def _opcion_ver_carpeta(self):
		"""Ver mensajes de una carpeta."""
		ruta = self._seleccionar_carpeta()
		if ruta:
			self._mostrar_mensajes_de_carpeta(ruta)
	
	def _opcion_buscar_mensajes(self):
		"""Buscar mensajes por texto."""
		texto = input("Texto a buscar: ").strip().lower()
		if not texto:
			print("Debe ingresar un texto.")
			return
		resultados = self.usuario.buscar_mensajes(
			lambda mensaje: texto in mensaje.mostrar_asunto.lower() or 
			               texto in mensaje.mostrar_cuerpo.lower()
		)
		if not resultados:
			print("Sin coincidencias.")
			return
		for idx, mensaje in enumerate(resultados, 1):
			print(f"{idx}. {mensaje.mostrar_resumen()}")
	
	def _opcion_mover_mensajes(self):
		"""Mover mensajes según criterio."""
		texto = input("Texto que identifica los mensajes a mover: ").strip().lower()
		destino = input("Carpeta destino (use / para subcarpetas): ").strip()
		if not texto or not destino:
			print("Texto y destino son obligatorios.")
			return
		origen = input("Carpeta origen (Enter para buscar en todas): ").strip() or None
		crear_dest = input("¿Crear carpeta destino si no existe? (s/n): ").strip().lower() in {"s", "si", "y"}
		try:
			movidos = self.usuario.mover_mensajes(
				lambda mensaje: texto in mensaje.mostrar_asunto.lower() or 
				               texto in mensaje.mostrar_cuerpo.lower(),
				destino, origen_ruta=origen, crear_destino=crear_dest
			)
			print(f"Se movieron {movidos} mensajes.")
		except (ValueError, LookupError) as e:
			print(f"Error: {e}")
	
	def _opcion_crear_carpeta(self):
		"""Crear nueva carpeta."""
		ruta = input("Nombre completo de la nueva carpeta (Ej: Entrada/Proyectos): ").strip()
		if not ruta:
			print("La ruta no puede estar vacía.")
			return
		try:
			self.usuario.obtener_o_crear_carpeta(ruta)
			print(f"Carpeta '{ruta}' disponible.")
		except ValueError as e:
			print(f"Error: {e}")
	
	def _opcion_agregar_filtro(self):
		"""Agregar filtro por asunto."""
		nombre = input("Nombre del filtro: ").strip()
		palabra = input("Palabra clave en el asunto: ").strip().lower()
		destino = input("Carpeta destino: ").strip()
		crear_dest = input("¿Crear carpeta destino si no existe? (s/n): ").strip().lower() in {"s", "si", "y"}
		if not nombre or not palabra or not destino:
			print("Todos los campos son obligatorios.")
			return
		try:
			self.usuario.agregar_filtro(
				nombre,
				lambda mensaje, palabra=palabra: palabra in mensaje.mostrar_asunto.lower(),
				destino, crear_destino=crear_dest
			)
			print("Filtro agregado.")
		except ValueError as e:
			print(f"Error: {e}")
	
	def _opcion_listar_filtros(self):
		"""Listar filtros activos."""
		filtros = self.usuario.listar_filtros()
		if not filtros:
			print("No hay filtros activos.")
		else:
			print("Filtros activos:")
			for nombre in filtros:
				print(f"- {nombre}")
	
	def _seleccionar_carpeta(self):
		"""Permite seleccionar una carpeta de la lista."""
		rutas = self.usuario.listar_carpetas()
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
	
	def _mostrar_mensajes_de_carpeta(self, ruta):
		"""Muestra los mensajes de una carpeta específica."""
		carpeta = self.usuario.obtener_carpeta(ruta)
		if carpeta is None:
			print("La carpeta no existe.")
			return
		mensajes = carpeta.listar_mensajes()
		if not mensajes:
			print("La carpeta está vacía.")
			return
		for idx, mensaje in enumerate(mensajes, 1):
			print(f"{idx}. {mensaje.mostrar_resumen()}")
