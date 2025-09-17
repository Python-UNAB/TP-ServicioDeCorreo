# TP - Servidor de Correo

Este proyecto provee una base orientada a objetos para un servidor de correo simple.

## Objetivos

- Clases principales: `Usuario`, `Mensaje`, `Carpeta`, `ServidorCorreo`.
- Encapsulamiento mediante propiedades y métodos de acceso.
- Documentación con diagrama de clases .

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
        -contenido: str
        -fecha: datetime
        +mostrar()
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
