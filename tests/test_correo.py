import pytest

from app.mensaje import Mensaje
from app.servidor import ServidorCorreo
from app.usuario import Usuario


def test_busqueda_recursiva_mensajes():
	test_user = Usuario("alice", "secret")
	carpeta_profunda = test_user.obtener_o_crear_carpeta("Entrada/Proyecto/2025")
	mensaje = Mensaje("alice", "alice", "Proyecto Final", "Detalles del proyecto")
	carpeta_profunda.agregar_mensaje(mensaje)
	resultados = test_user.buscar_mensajes(lambda m: "proyecto" in m.mostrar_asunto.lower())
	assert mensaje in resultados


def test_mover_mensajes_recursivo():
	test_user = Usuario("bob", "secret")
	test_user.obtener_o_crear_carpeta("Entrada/Temporal")
	carpeta_origen = test_user.obtener_carpeta("Entrada/Temporal")
	mensaje = Mensaje("bob", "bob", "Reunión", "Agenda semanal")
	carpeta_origen.agregar_mensaje(mensaje)
	movidos = test_user.mover_mensajes(lambda m: "reunión" in m.mostrar_asunto.lower(), "Archivo/2024", origen_ruta="Entrada", crear_destino=True)
	assert movidos == 1
	carpeta_destino = test_user.obtener_carpeta("Archivo/2024")
	assert carpeta_destino is not None
	assert mensaje in carpeta_destino.listar_mensajes()
	assert mensaje not in carpeta_origen.listar_mensajes()


def test_filtro_automatico_mueve_a_carpeta():
	servidor = ServidorCorreo()
	servidor.registrar_usuario("alice", "secret")
	servidor.registrar_usuario("bob", "secret")
	usuario_bob = servidor.obtener_usuario("bob")
	usuario_bob.agregar_filtro("alertas", lambda m: "aviso" in m.mostrar_asunto.lower(), "Alertas", crear_destino=True)
	servidor.enviar_mensaje("alice", "bob", "Aviso Importante", "Revisar de inmediato")
	carpeta_alertas = usuario_bob.obtener_carpeta("Alertas")
	assert carpeta_alertas is not None
	mensajes_alertas = carpeta_alertas.listar_mensajes()
	assert len(mensajes_alertas) == 1
	assert mensajes_alertas[0].mostrar_asunto == "Aviso Importante"
	assert not usuario_bob.obtener_carpeta("Entrada").listar_mensajes()


def test_cola_prioridad_urgentes():
	servidor = ServidorCorreo()
	servidor.registrar_usuario("alice", "secret")
	servidor.registrar_usuario("bob", "secret")
	m1 = servidor.enviar_mensaje("alice", "bob", "Normal", "Mensaje", urgente=True, prioridad=1)
	m2 = servidor.enviar_mensaje("alice", "bob", "Crítico", "Mensaje", urgente=True, prioridad=0)
	assert servidor.tiene_mensajes_urgentes() is True
	primero = servidor.extraer_mensaje_urgente()
	segundo = servidor.extraer_mensaje_urgente()
	assert primero is m2
	assert segundo is m1
	assert servidor.extraer_mensaje_urgente() is None


def test_mover_mensajes_sin_resultados():
	usuario = Usuario("carol", "secret")
	usuario.obtener_carpeta("Entrada")
	usuario.obtener_o_crear_carpeta("Archivo")
	with pytest.raises(LookupError):
		usuario.mover_mensajes(lambda m: "inexistente" in m.mostrar_asunto.lower(), "Archivo")
