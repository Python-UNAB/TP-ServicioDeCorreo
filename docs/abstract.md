# Abstract

## Decisiones de diseño

### Arquitectura general

- **ServidorCorreo** centraliza registro, autenticación y enrutamiento de mensajes entre usuarios.
- **Usuario** posee carpetas predefinidas (Entrada, Enviados) para simplificar el flujo básico, y puede crear subcarpetas anidadas dinámicamente.
- **Mensaje** es inmutable en sus metadatos luego de creado; solo se muestra o resume.
- **Mensaje** incorpora prioridad opcional (rango 1-5) para integrarse con la cola de urgentes basada en heap.
- **Algorithms** reúne utilidades puras para búsqueda recursiva, recorridos (DFS/BFS) y ordenamiento de mensajes.
- **Modularización por archivos**: cada clase en su módulo (`usuario.py`, `mensaje.py`, `carpeta.py`, `servidor.py`), más `app/main.py` como punto de entrada.

### Estructura de árbol (recursividad)

- **Gestión recursiva de carpetas**: cada `Carpeta` puede contener subcarpetas formando un árbol.
- **Búsqueda y movimiento recursivos**: los métodos `buscar_mensajes` y `extraer_mensajes` recorren toda la jerarquía de subcarpetas para localizar y reubicar mensajes según criterios.
- **Recorridos DFS y BFS**: la clase `Carpeta` expone generadores explícitos para profundidad (`recorrer_dfs`) y amplitud (`recorrer_bfs`), y `Usuario` puede listar carpetas en cualquiera de los dos órdenes.
- **Rutas con barra**: las carpetas se identifican con rutas tipo `Entrada/Proyectos/2025`, navegadas recursivamente al crear o acceder.

### Filtros automáticos

- **Filtros declarativos**: cada regla se encapsula en la clase `Filtro`, centralizando nombre, condición, carpeta destino y configuración de creación automática.
- **Enrutamiento automático**: al recibir un mensaje, se aplican los filtros del usuario; si uno coincide, el mensaje se mueve de Entrada a la carpeta destino configurada.

### Cola de mensajes urgentes (Heap)

- **Heap de prioridad mínima**: se usa `heapq` para ordenar mensajes según prioridad numérica (1 = mayor urgencia, 5 = menor) manteniendo el orden de llegada en empates.
- **Visualización en menú de usuario**: opción dedicada para listar y atender todos los urgentes pendientes.

### Correcciones aplicadas (para las entregas)

- **Modularización**: archivos separados por clase según recomendación del profesor.
- **Recursividad implementada**: búsqueda y movimiento funcionan en toda la jerarquía de carpetas.
- **Tests unitarios**: 5 pruebas que validan recursividad, filtros, cola de urgentes y casos límite.
- **Casos límite documentados**: carpetas inexistentes, búsquedas vacías, filtros sin destino.

## Alcance de esta entrega

- Implementación de recursividad.
- Implementación de estructura de Arboles.
- Implementación de Test para verificar el correcto funcionamiento.
- Funcionalidades de consola: registro, autenticación, envío, búsqueda, movimiento, filtros, urgentes.
- Implementación de generadores DFS/BFS en `Carpeta` para iterar el árbol de forma completa.
- Mejora de legibilidad del codigo implementando las importaciones de typing, esto permite la detección de errores.
- Integración de heap para manejar prioridades de mensajes urgentes.
