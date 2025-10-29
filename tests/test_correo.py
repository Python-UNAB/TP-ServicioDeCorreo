import pytest

from app.mensaje import Mensaje
from app.servidor import ServidorCorreo
from app.usuario import Usuario


def test_busqueda_recursiva_mensajes():
	test_user = Usuario("Miguel", "secret")
	carpeta_profunda = test_user.obtener_o_crear_carpeta("Entrada/Proyecto/2025")
	mensaje = Mensaje("Miguel", "Miguel", "Proyecto Final", "Detalles del proyecto")
	carpeta_profunda.agregar_mensaje(mensaje)
	resultados = test_user.buscar_mensajes(lambda m: "proyecto" in m.mostrar_asunto.lower())
	assert mensaje in resultados


def test_mover_mensajes_recursivo():
	test_user = Usuario("Rodrigo", "secret")
	test_user.obtener_o_crear_carpeta("Entrada/Temporal")
	carpeta_origen = test_user.obtener_carpeta("Entrada/Temporal")
	mensaje = Mensaje("Rodrigo", "Rodrigo", "Reunión", "Agenda semanal")
	carpeta_origen.agregar_mensaje(mensaje)
	movidos = test_user.mover_mensajes(lambda m: "reunión" in m.mostrar_asunto.lower(), "Archivo/2024", origen_ruta="Entrada", crear_destino=True)
	assert movidos == 1
	carpeta_destino = test_user.obtener_carpeta("Archivo/2024")
	assert carpeta_destino is not None
	assert mensaje in carpeta_destino.listar_mensajes()
	assert mensaje not in carpeta_origen.listar_mensajes()


def test_filtro_automatico_mueve_a_carpeta():
	servidor = ServidorCorreo()
	servidor.registrar_usuario("Miguel", "secret")
	servidor.registrar_usuario("Rodrigo", "secret")
	usuario_Rodrigo = servidor.obtener_usuario("Rodrigo")
	usuario_Rodrigo.agregar_filtro("alertas", lambda m: "aviso" in m.mostrar_asunto.lower(), "Alertas", crear_destino=True)
	servidor.enviar_mensaje("Miguel", "Rodrigo", "Aviso Importante", "Revisar de inmediato")
	carpeta_alertas = usuario_Rodrigo.obtener_carpeta("Alertas")
	assert carpeta_alertas is not None
	mensajes_alertas = carpeta_alertas.listar_mensajes()
	assert len(mensajes_alertas) == 1
	assert mensajes_alertas[0].mostrar_asunto == "Aviso Importante"
	assert not usuario_Rodrigo.obtener_carpeta("Entrada").listar_mensajes()


def test_cola_prioridad_urgentes():
	servidor = ServidorCorreo()
	servidor.registrar_usuario("Miguel", "secret")
	servidor.registrar_usuario("Rodrigo", "secret")
	m1 = servidor.enviar_mensaje("Miguel", "Rodrigo", "Mensaje 1", "Contenido 1", urgente=True)
	m2 = servidor.enviar_mensaje("Miguel", "Rodrigo", "Mensaje 2", "Contenido 2", urgente=True)
	m3 = servidor.enviar_mensaje("Miguel", "Rodrigo", "Mensaje 3", "Contenido 3", urgente=True)
	assert servidor.tiene_mensajes_urgentes() is True
	# La cola extrae del más viejo al más reciente (FIFO)
	primero = servidor.extraer_mensaje_urgente()
	segundo = servidor.extraer_mensaje_urgente()
	tercero = servidor.extraer_mensaje_urgente()
	assert primero is m1  # El primero enviado es el primero extraído
	assert segundo is m2
	assert tercero is m3
	assert servidor.extraer_mensaje_urgente() is None


def test_mover_mensajes_sin_resultados():
	usuario = Usuario("Juan", "secret")
	usuario.obtener_carpeta("Entrada")
	usuario.obtener_o_crear_carpeta("Archivo")
	with pytest.raises(LookupError):
		usuario.mover_mensajes(lambda m: "inexistente" in m.mostrar_asunto.lower(), "Archivo")
