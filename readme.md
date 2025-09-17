# TP - Servidor de Correo (Código base)

Se va a desarrollar un modelo de servidor de correo, donde el usuario debera registrarse y enviara mensajes a otros usuarios registrados dentro del servidor.
Por defecto se dejo configurado un usuario registrado para la verificación de funcionalidad del mismo.

## Objetivos

- Clases principales: `Usuario`, `Mensaje`, `Carpeta`, `ServidorCorreo`.
- Encapsulamiento mediante propiedades y métodos de acceso.
- Interfaces para enviar, recibir y listar mensajes (ABCs: `IEnviador`, `IReceptor`, `IListador`).
- Documentación con diagrama de clases y justificación de diseño.

## Diagrama de clases (UML)

```mermaid
classDiagram
    direction TB

    class ServidorCorreo {
        -usuarios: List~Usuario~
        +registrar_usuario()
        +autenticar()
        +enviar_mensaje()
    }

    class Usuario {
        -username: str
        -password: str
        -carpetas: List~Carpeta~
        +ver_carpetas()
        +ver_mensajes()
    }

		class Carpeta {
			-nombre: str
			-mensajes: List~Mensaje~
			+agregar(m: Mensaje) void
			+eliminar(id_mensaje: str) Mensaje
			+mensajes() List~Mensaje~
			+contar_no_leidos() int
		}

		class Usuario {
			-email: str
			-nombre: str
			-carpetas: Dict~str, Carpeta~
			+obtener_carpeta(nombre: str) Carpeta
			+listar_carpetas() List~str~
		}

		class ServidorCorreo {
			-usuarios: Dict~str, Usuario~
			+registrar_usuario(u: Usuario) void
			+obtener_usuario(email: str) Usuario
		}

		IEnviador <|.. ServidorCorreo
		IReceptor <|.. ServidorCorreo
		IListador <|.. ServidorCorreo

		Usuario "1" o-- "*" Carpeta
		Carpeta "1" o-- "*" Mensaje
		Mensaje "1" --> "1" Usuario : remitente
		ServidorCorreo "1" o-- "*" Usuario
```

## Justificación de decisiones

- Interfaces como ABCs: Permiten definir contratos claros para enviar, recibir y listar, habilitando reemplazos o mocks en pruebas sin acoplar al servidor.
- Encapsulamiento: Atributos con guion bajo y acceso por propiedades evitan modificar el estado interno inadvertidamente y facilitan validaciones futuras sin romper clientes.
- Carpeta on-demand: `Usuario.obtener_carpeta` crea carpetas dinámicamente para flexibilidad; aun así se inicializan `Entrada`, `Enviados` y `Papelera` por defecto.
- Inmutabilidad parcial de `Mensaje`: La mayoría de atributos son de solo lectura; el estado de lectura cambia con `marcar_leido` para mantener el historial consistente.
- Identidad con UUID: `Mensaje` usa IDs únicos para operaciones como eliminar o trazar.

## Cómo probar rápidamente

Ejecuta el demo incluido:

```powershell
# Windows PowerShell
python .\app.py
```

Deberías ver listados de la bandeja de entrada y enviados de dos usuarios de ejemplo.

## Próximos pasos sugeridos

- Validaciones de formato de email y normalización.
- Búsqueda y filtrado (por remitente, asunto, fecha, leído/no leído).
- Persistencia (archivos JSON, SQLite) y repositorios.
