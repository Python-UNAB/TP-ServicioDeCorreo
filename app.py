"""
Servidor de correo - código base

Este módulo define:
- Clases principales: Usuario, Mensaje, Carpeta, ServidorCorreo
- Interfaces (ABCs) para enviar, recibir y listar mensajes
- Encapsulamiento mediante propiedades
- Un pequeño demo si se ejecuta como script
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Iterable, List, Optional
import uuid


# =============================
# Interfaces (contratos)
# =============================


class IEnviador(ABC):
	"""Contrato para enviar mensajes."""

	@abstractmethod
	def enviar_mensaje(self, remitente: "Usuario", destinatario_email: str, asunto: str, cuerpo: str) -> "Mensaje":
		"""Envía un mensaje desde un remitente a un destinatario (por email)."""
		raise NotImplementedError


class IReceptor(ABC):
	"""Contrato para recibir mensajes (entregar a la bandeja del usuario)."""

	@abstractmethod
	def recibir_mensaje(self, destinatario: "Usuario", mensaje: "Mensaje") -> None:
		"""Recibe un mensaje y lo entrega a la carpeta de entrada del destinatario."""
		raise NotImplementedError


class IListador(ABC):
	"""Contrato para listar mensajes de un usuario y carpeta."""

	@abstractmethod
	def listar_mensajes(self, usuario: "Usuario", nombre_carpeta: str = "Entrada") -> Iterable["Mensaje"]:
		"""Lista los mensajes de la carpeta indicada para un usuario."""
		raise NotImplementedError


# =============================
# Entidades del dominio
# =============================


class Mensaje:
	"""Representa un mensaje de correo."""

	def __init__(
		self,
		remitente: "Usuario",
		destinatario_email: str,
		asunto: str,
		cuerpo: str,
		fecha: Optional[datetime] = None,
		id_: Optional[str] = None,
	) -> None:
		self._id = id_ or str(uuid.uuid4())
		self._remitente = remitente
		self._destinatario_email = destinatario_email
		self._asunto = asunto
		self._cuerpo = cuerpo
		self._fecha = fecha or datetime.now()
		self._leido = False

	# Propiedades de solo lectura (salvo leido)
	@property
	def id(self) -> str:
		return self._id

	@property
	def remitente(self) -> "Usuario":
		return self._remitente

	@property
	def destinatario_email(self) -> str:
		return self._destinatario_email

	@property
	def asunto(self) -> str:
		return self._asunto

	@property
	def cuerpo(self) -> str:
		return self._cuerpo

	@property
	def fecha(self) -> datetime:
		return self._fecha

	@property
	def leido(self) -> bool:
		return self._leido

	def marcar_leido(self) -> None:
		self._leido = True

	def __repr__(self) -> str:  # útil para listar en consola
		estado = "✓" if self._leido else "·"
		return f"Mensaje({estado} {self._fecha:%Y-%m-%d %H:%M} - {self._asunto!r} de {self._remitente.email} a {self._destinatario_email})"


class Carpeta:
	"""Agrupa mensajes de un usuario (Entrada, Enviados, Papelera, etc.)."""

	def __init__(self, nombre: str) -> None:
		self._nombre = nombre
		self._mensajes: List[Mensaje] = []

	@property
	def nombre(self) -> str:
		return self._nombre

	def agregar(self, mensaje: Mensaje) -> None:
		self._mensajes.append(mensaje)

	def eliminar(self, id_mensaje: str) -> Optional[Mensaje]:
		for i, m in enumerate(self._mensajes):
			if m.id == id_mensaje:
				return self._mensajes.pop(i)
		return None

	def mensajes(self) -> List[Mensaje]:
		"""Devuelve una copia para evitar modificación externa directa."""
		return list(self._mensajes)

	def contar_no_leidos(self) -> int:
		return sum(1 for m in self._mensajes if not m.leido)

	def __repr__(self) -> str:
		return f"Carpeta({self._nombre}, {len(self._mensajes)} mensajes)"


class Usuario:
	"""Representa un usuario del sistema de correo."""

	def __init__(self, email: str, nombre: str) -> None:
		self._email = email
		self._nombre = nombre
		# Carpeta por defecto
		self._carpetas: Dict[str, Carpeta] = {
			"Entrada": Carpeta("Entrada"),
			"Enviados": Carpeta("Enviados"),
			"Papelera": Carpeta("Papelera"),
		}

	@property
	def email(self) -> str:
		return self._email

	@property
	def nombre(self) -> str:
		return self._nombre

	def obtener_carpeta(self, nombre: str) -> Carpeta:
		if nombre not in self._carpetas:
			# Creamos carpeta on-demand para flexibilidad
			self._carpetas[nombre] = Carpeta(nombre)
		return self._carpetas[nombre]

	def listar_carpetas(self) -> List[str]:
		return sorted(self._carpetas.keys())

	def __repr__(self) -> str:
		return f"Usuario({self._email}, {self._nombre})"


# =============================
# Servicio principal
# =============================


class ServidorCorreo(IEnviador, IReceptor, IListador):
	"""Gestiona usuarios y operaciones de correo (enviar/recibir/listar)."""

	def __init__(self) -> None:
		self._usuarios: Dict[str, Usuario] = {}

	# Gestión de usuarios
	def registrar_usuario(self, usuario: Usuario) -> None:
		if usuario.email in self._usuarios:
			raise ValueError(f"El usuario {usuario.email} ya existe")
		self._usuarios[usuario.email] = usuario

	def obtener_usuario(self, email: str) -> Optional[Usuario]:
		return self._usuarios.get(email)

	# Implementación de IEnviador
	def enviar_mensaje(self, remitente: Usuario, destinatario_email: str, asunto: str, cuerpo: str) -> Mensaje:
		if remitente.email not in self._usuarios:
			raise ValueError("Remitente no registrado en el servidor")
		if destinatario_email not in self._usuarios:
			raise ValueError("Destinatario no registrado en el servidor")

		mensaje = Mensaje(remitente=remitente, destinatario_email=destinatario_email, asunto=asunto, cuerpo=cuerpo)

		# Guardar en 'Enviados' del remitente
		remitente.obtener_carpeta("Enviados").agregar(mensaje)

		# Entregar al destinatario
		destinatario = self._usuarios[destinatario_email]
		self.recibir_mensaje(destinatario, mensaje)

		return mensaje

	# Implementación de IReceptor
	def recibir_mensaje(self, destinatario: Usuario, mensaje: Mensaje) -> None:
		destinatario.obtener_carpeta("Entrada").agregar(mensaje)

	# Implementación de IListador
	def listar_mensajes(self, usuario: Usuario, nombre_carpeta: str = "Entrada") -> Iterable[Mensaje]:
		return usuario.obtener_carpeta(nombre_carpeta).mensajes()


# =============================
# Demo rápido
# =============================


def _demo() -> None:
	print("Demo: Servidor de Correo")
	servidor = ServidorCorreo()

	# Crear y registrar usuarios
	alice = Usuario("alice@example.com", "Alice")
	bob = Usuario("bob@example.com", "Bob")
	servidor.registrar_usuario(alice)
	servidor.registrar_usuario(bob)

	# Enviar un par de mensajes
	servidor.enviar_mensaje(alice, "bob@example.com", "Hola Bob", "¿Nos vemos mañana?")
	servidor.enviar_mensaje(bob, "alice@example.com", "Re: Hola Bob", "Claro, a las 10.")

	# Listar bandeja de entrada de Alice
	print("\nBandeja de entrada de Alice:")
	for m in servidor.listar_mensajes(alice, "Entrada"):
		print("-", m)

	# Listar enviados de Bob
	print("\nEnviados de Bob:")
	for m in servidor.listar_mensajes(bob, "Enviados"):
		print("-", m)


if __name__ == "__main__":
	_demo()


