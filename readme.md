# TP - Servidor de Correo

- Se realizaron las correcciones solicitadas en la ultima entrega con respecto a la lógica de recursividad de las carpetas y subcarpetas permitiendo las operaciones de busqueda y movimiento de mensajes.
- Se integró la librería de "pytest" para verificar el correcto funcionamiento del servidor y hacer pruebas límites.
- Se amplió el Abstract.md para mejorar la documentación del código, en caso de que aún debamos completar cosas por favor comentarlos en la devolución.

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
- **Cola de urgentes (heap)**: cada usuario mantiene su propio heap; las inserciones se realizan con `heapq` en `O(log n)` y las extracciones priorizan el menor valor (rango permitido 1-5), usando un contador para mantener el orden de llegada en empates.

## Algoritmos reutilizables

- `src/algorithms/busqueda_recursiva.py`: funciones puras para localizar y extraer mensajes recorriendo el árbol.
- `src/algorithms/ordenamiento.py`: estrategias de ordenamiento por fecha o prioridad aplicables a cualquier lista de mensajes.
- `src/algorithms/recorrido_grafo.py`: generadores DFS/BFS para iterar la jerarquía de carpetas.

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
        -__usuarios: Dict~str, Usuario~
        +registrar_usuario(username, password)
        +autenticar(username, password) Usuario
        +obtener_usuario(username) Usuario
        +enviar_mensaje(remitente, destinatario, asunto, cuerpo, urgente, prioridad)
    }

    class Usuario {
        -__username: str
        -__password: str
        -__carpetas: Dict~str, Carpeta~
        -__filtros: List~Filtro~
        -__cola_urgentes: List~Tuple~int, int, Mensaje~~
        +username: str
        +password: str
        +obtener_carpeta(ruta) Carpeta
        +obtener_o_crear_carpeta(ruta) Carpeta
        +listar_carpetas(orden='dfs') List~str~
        +buscar_mensajes(criterio, carpeta_ruta)
        +mover_mensajes(criterio, destino_ruta, origen_ruta) int
        +agregar_filtro(nombre, condicion, destino_ruta)
        +listar_filtros() List~str~
        +aplicar_filtros(mensaje) str
        +registrar_mensaje_urgente(mensaje)
        +tiene_mensajes_urgentes() bool
        +extraer_mensaje_urgente() Mensaje
    }

    class Filtro {
        -__nombre: str
        -__condicion: Callable
        -__destino_ruta: str
        -__crear_destino: bool
        +nombre: str
        +destino_ruta: str
        +crear_destino: bool
        +aplica_a(mensaje) bool
    }

    class Carpeta {
        -__nombre_carpeta: str
        -__mensajes: List~Mensaje~
        -__subcarpetas: Dict~str, Carpeta~
        +nombre: str
        +agregar_mensaje(mensaje)
        +agregar_mensajes(mensajes)
        +listar_mensajes() List~Mensaje~
        +eliminar_mensaje(mensaje) bool
        +crear_subcarpeta(nombre) Carpeta
        +obtener_subcarpeta(nombre) Carpeta
        +listar_subcarpetas() Dict
        +buscar_mensajes(criterio) List~Mensaje~
        +extraer_mensajes(criterio) List~Mensaje~
        +recorrer() Generator
    }

    class Mensaje {
        -__remitente: Usuario
        -__destinatario: Usuario
        -__asunto: str
        -__cuerpo: str
        -__fecha: datetime
        -__urgente: bool
        -__prioridad: Optional~int~
        +mostrar_remitente: str
        +mostrar_destinatario: str
        +mostrar_asunto: str
        +mostrar_cuerpo: str
        +fecha: datetime
        +es_urgente: bool
        +prioridad: Optional~int~
        +mostrar_correo() str
        +mostrar_resumen() str
    }

    ServidorCorreo "1" o-- "*" Usuario : gestiona
    Usuario "1" o-- "*" Carpeta : contiene
    Usuario "1" o-- "*" Filtro : aplica
    Carpeta "1" o-- "*" Mensaje : almacena
    Carpeta "1" o-- "*" Carpeta : subcarpetas
    Mensaje "*" --> "1" Usuario : remitente
    Mensaje "*" --> "1" Usuario : destinatario
```

## Cómo probar rápidamente

Ejecuta el demo incluido:

```powershell
# Windows PowerShell
python -m src.ui.main
```

## Pruebas automáticas

Se añadieron pruebas unitarias con `pytest` para cubrir la búsqueda recursiva, el movimiento de mensajes, la aplicación de filtros y la cola de urgentes.

```bash
pip install pytest  # en caso de no tenerlo instalado
pytest -q
```

## Manual de uso

- Ejecutar el código con `python -m src.ui.main` desde la raíz del proyecto.
- Seleccionar alguna de las opciones listadas en el menú:
  - **Registrarse o ingresar** con usuario y contraseña.
    - **Enviar mensajes** asignando prioridad numérica del 1 al 5 (1 = más urgente) cuando sea necesario.
    - **Ver mensajes** de cualquier carpeta listada, seleccionándola por número y luego el mensaje deseado.
  - **Crear subcarpetas** anidadas (ejemplo: `Entrada/Proyectos/2025`).
  - **Buscar y mover mensajes** por texto en asunto o cuerpo, de forma recursiva en toda la jerarquía.
  - **Configurar filtros** por asunto para organizar la bandeja automáticamente.
    - **Ver mensajes urgentes** en la bandeja personal del usuario (se extraen respetando prioridad y orden de llegada).

## Modalidad de trabajo:

- Se colaboró en conjunto, y se trabajó con LiveShare permitiendo un desarrollo coordinado.

## Grupo 7

- Miguel Miguez
- Rodrigo Podoba
- Juan Rubio
