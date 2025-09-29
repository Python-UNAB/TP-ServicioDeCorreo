# TP - Servidor de Correo

Se realizaron las correcciones solicitadas en la primer entrega, respecto a la modularización del proyecto para incrementar la mantenibilidad del código. Ademas se agregó la carpeta docs con un archivo abstract.md donde se argumentan las desiciones del diseño.

## Objetivos

- Modelar las clases principales: ServidorCorreo, Usuario, Carpeta y Mensaje.
- Aplicar encapsulamiento mediante atributos privados y propiedades/métodos de acceso.
- Implementar una interfaz mínima de interacción (registro, autenticación y envío/listado de mensajes).
- Ver también el [Abstract](./docs/abstract.md) con objetivos, decisiones y alcance.

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
python -m app.main
```

## Manual de uso:

- Ejecutar el codigo
- Seleccionar alguna de las opciones listadas del menú

## Proximos pasos:

- Implementar menú con el Framework tkinter
- Gestionar el envío de mensajes con un metodo "enviar_mensaje"
- Implementación del método de mostrar_resumen

## Modalidad de trabajo:

- Se colaboró en conjunto, y se trabajó con LiveShare permitiendo un desarrollo coordinado.
