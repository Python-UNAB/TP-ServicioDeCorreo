# Abstract

## Decisiones de diseño

### Arquitectura general

- **ServidorCorreo** centraliza registro, autenticación y enrutamiento de mensajes entre usuarios.
- **Usuario** posee carpetas predefinidas (Entrada, Enviados) para simplificar el flujo básico, y puede crear subcarpetas anidadas dinámicamente.
- **Mensaje** es inmutable en sus metadatos luego de creado; solo se muestra o resume.
- **Modularización por archivos**: cada clase en su módulo (`usuario.py`, `mensaje.py`, `carpeta.py`, `servidor.py`), más `app/main.py` como punto de entrada.

### Estructura de árbol (recursividad)

- **Gestión recursiva de carpetas**: cada `Carpeta` puede contener subcarpetas formando un árbol arbitrario.
- **Búsqueda y movimiento recursivos**: los métodos `buscar_mensajes` y `extraer_mensajes` recorren toda la jerarquía de subcarpetas para localizar y reubicar mensajes según criterios.
- **Rutas con barra**: las carpetas se identifican con rutas tipo `Entrada/Proyectos/2025`, navegadas recursivamente al crear o acceder.

### Filtros automáticos

- **Filtros declarativos**: lista de reglas (diccionarios) que evalúan cada mensaje entrante.
- **Enrutamiento automático**: al recibir un mensaje, se aplican los filtros del usuario; si uno coincide, el mensaje se mueve de Entrada a la carpeta destino configurada.

### Cola de mensajes urgentes (FIFO)

- **Sin prioridad numérica**: se eliminó el concepto de prioridad numérica (0, 1, 2...).
- **Cola simple FIFO**: mensajes urgentes se insertan al inicio de una lista; al extraer se toma del final (el más viejo primero), manteniendo orden de llegada.
- **Visualización en menú de usuario**: opción dedicada para listar y atender todos los urgentes pendientes.

### Correcciones aplicadas (segunda entrega)

- **Modularización**: archivos separados por clase según recomendación del profesor.
- **Abstract agregado**: este documento con objetivos, decisiones y alcance.
- **Recursividad implementada**: búsqueda y movimiento funcionan en toda la jerarquía de carpetas.
- **Tests unitarios**: 5 pruebas que validan recursividad, filtros, cola de urgentes y casos límite.
- **Documentación de complejidad**: análisis Big-O de operaciones principales en README.
- **Casos límite documentados**: carpetas inexistentes, búsquedas vacías, filtros sin destino.

## Alcance de esta entrega

- Implementación en memoria sin persistencia.
- Funcionalidades de consola: registro, autenticación, envío, búsqueda, movimiento, filtros, urgentes.
- Base lista para extender con validaciones, persistencia (JSON/SQLite) y UI gráfica (tkinter/Flask).
