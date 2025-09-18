# TP - Servidor de Correo (Primera entrega)

Se va a desarrollar un modelo de servidor de correo, donde el usuario debera registrarse y enviara mensajes a otros usuarios registrados dentro del servidor.
Por defecto se dejo configurado un usuario registrado para la verificación de funcionalidad del mismo.

## Objetivos

- Clases principales: `Usuario`, `Mensaje`, `Carpeta`, `ServidorCorreo`.
- Encapsulamiento mediante propiedades y métodos de acceso.
- Documentación con diagrama de clases.


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
        +agregar_mensaje()
        +listar_mensajes()
    }

    class Mensaje {
        -remitente: Usuario
        -destinatario: Usuario
        -asunto: str
        -cuerpo: str
		-fecha: datetime.now()
        +mostrar_remitente()
		+mostrar_destinatario()
		+mostrar_asunto()
		+mostrar_cuerpo()
		+mostrar_correo()
		+mostrar_resumen() #Este método fue pensado para resumir un correo completo
    }

    ServidorCorreo "1" o-- "*" Usuario
    Usuario "1" o-- "*" Carpeta
    Carpeta "1" o-- "*" Mensaje
    Mensaje "1" --> "1" Usuario : remitente
    Mensaje "1" --> "1" Usuario : destinatario
```

## Cómo probar rápidamente

Ejecuta el demo incluido:

```powershell
# Windows PowerShell
python .\app.py
```

## Manual de uso:

- Ejecutar el codigo
- Seleccionar alguna de las opciones listadas del menú

## Proximos pasos:

- Implementar menú con el Framework tkinter
- Realizar diagrama de flujo en Figma. 
- Gestionar el envío de mensajes con un metodo "enviar_mensaje"
- Implementación del método de mostrar_resumen

## Modalidad de trabajo:
	- Se colaboró en conjunto, y se trabajó con LiveShare permitiendo un desarrollo coordinado.
