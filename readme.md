# TP - Servidor de Correo

Se realizaron las correcciones solicitadas en la primer entrega, respecto a la modularización del proyecto para incrementar la mantenibilidad del código. Ademas se agregó la carpeta docs con un archivo abstract.md donde se argumentan las decisiones del diseño.
Ademas se implementó el metodo para enviar mensajes.

## Objetivos

- Modelar las clases principales: ServidorCorreo, Usuario, Carpeta y Mensaje.
- Aplicar encapsulamiento mediante atributos privados y propiedades/métodos de acceso.
- Implementar una interfaz mínima de interacción (registro, autenticación y envío/listado de mensajes).
- Ver también el [Abstract](./docs/abstract.md) con objetivos, decisiones y alcance.
- Automatizar la clasificación de mensajes mediante filtros configurables por usuario.
- Priorizar mensajes urgentes utilizando una cola de prioridad dedicada.

## Complejidad y eficiencia

- **Búsqueda recursiva**: la búsqueda recorre todas las carpetas y subcarpetas de forma recursiva. En el peor caso es `O(n)` donde `n` es la cantidad total de mensajes almacenados en todo el árbol de carpetas.
- **Movimiento de mensajes**: la extracción y reubicación también recorre recursivamente, con complejidad `O(n)` en el peor caso si se visita cada carpeta del árbol.
- **Aplicación de filtros**: por cada mensaje recibido se evalúan las reglas configuradas (`O(r)` donde `r` es la cantidad de filtros del usuario). La evaluación se detiene cuando un filtro coincide.
- **Cola de urgentes (FIFO)**: las inserciones al inicio y extracciones al final de la lista son `O(1)` amortizado. No se usa prioridad numérica; el orden es por llegada (primero en llegar, primero en salir).

## Casos límite considerados

- **Carpetas inexistentes**: al intentar mover mensajes hacia una carpeta que no existe, el sistema informa el error o crea la carpeta automáticamente según la configuración del usuario.
- **Búsquedas sin resultados**: se devuelve una lista vacía sin generar errores.
- **Cola de urgentes vacía**: al consultar mensajes urgentes cuando no hay ninguno pendiente, se informa al usuario sin fallar.
- **Filtros con carpetas destino ausentes**: pueden crearse automáticamente (si `crear_destino=True`) o ignorarse si el usuario prefiere no crear carpetas nuevas.

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

## Pruebas automáticas

Se añadieron pruebas unitarias con `pytest` para cubrir la búsqueda recursiva, el movimiento de mensajes, la aplicación de filtros y la cola de urgentes.

```bash
pip install pytest  # en caso de no tenerlo instalado
pytest -q
```

## Manual de uso

- Ejecutar el código con `python -m app.main` desde la raíz del proyecto.
- Seleccionar alguna de las opciones listadas en el menú:
  - **Registrarse o ingresar** con usuario y contraseña.
  - **Enviar mensajes** a otros usuarios registrados, marcándolos como urgentes si es necesario.
  - **Ver mensajes** de Entrada o Enviados, seleccionando un mensaje para leer el contenido completo.
  - **Crear subcarpetas** anidadas (ejemplo: `Entrada/Proyectos/2025`).
  - **Buscar y mover mensajes** por texto en asunto o cuerpo, de forma recursiva en toda la jerarquía.
  - **Configurar filtros** por asunto para organizar la bandeja automáticamente.
  - **Ver mensajes urgentes** pendientes desde el menú de usuario (se extraen en orden de llegada).

## Próximos pasos

- Implementar interfaz gráfica con tkinter o web con Flask.
- Persistencia en archivo JSON o base de datos SQLite.
- Validaciones adicionales (formato de email, longitud de mensajes).
- Notificaciones push o email real para nuevos mensajes.

## Modalidad de trabajo:

- Se colaboró en conjunto, y se trabajó con LiveShare permitiendo un desarrollo coordinado.
