# Abstract

## Decisiones de diseño

### Arquitectura general

- **ServidorCorreo** centraliza registro, autenticación y enrutamiento de mensajes entre usuarios.
- **Usuario** posee carpetas predefinidas (Entrada, Enviados) para simplificar el flujo básico, y puede crear subcarpetas anidadas dinámicamente.
- **Mensaje** es inmutable en sus metadatos luego de creado; solo se muestra o resume.
- **Modularización completa**: el proyecto ha sido refactorizado a una arquitectura de capas en `src/` (models, algorithms, services, ui).

### Refactorización Arquitectónica (Nueva Entrega)

El sistema ha sido completamente reestructurado siguiendo principios de diseño modular:

#### Capa de Modelos (`src/models/`)

- Representación del dominio: Usuario, Mensaje, Carpeta, ServidorCorreo
- Encapsulamiento completo con type hints
- Inmutabilidad donde corresponde

#### Capa de Algoritmos (`src/algorithms/`)

- Búsqueda recursiva con análisis O(n)
- Ordenamiento Timsort O(n log n)
- Recorridos BFS/DFS para estructuras de carpetas
- Documentación de complejidad en cada algoritmo

#### Capa de Servicios (`src/services/`)

- GestorMensajes: operaciones de alto nivel
- GestorCarpetas: gestión de estructura jerárquica
- GestorFiltros: factory de filtros automáticos
- GestorRed: base para sistema distribuido (futuro)

#### Capa de Presentación (`src/ui/`)

- Separación CLI en MenuPrincipal y MenuUsuario
- Preparado para reemplazo con GUI (tkinter)

### Estructura de árbol (recursividad)

- **Gestión recursiva de carpetas**: cada `Carpeta` puede contener subcarpetas formando un árbol.
- **Búsqueda y movimiento recursivos**: los métodos `buscar_mensajes` y `extraer_mensajes` recorren toda la jerarquía de subcarpetas para localizar y reubicar mensajes según criterios.
- **Rutas con barra**: las carpetas se identifican con rutas tipo `Entrada/Proyectos/2025`, navegadas recursivamente al crear o acceder.

### Filtros automáticos

- **Filtros declarativos**: lista de reglas (diccionarios) que evalúan cada mensaje entrante.
- **Enrutamiento automático**: al recibir un mensaje, se aplican los filtros del usuario; si uno coincide, el mensaje se mueve de Entrada a la carpeta destino configurada.
- **Factory de filtros**: GestorFiltros proporciona creadores de filtros comunes (por asunto, remitente, urgencia)

### Cola de mensajes urgentes

- **Heap de prioridad**: mensajes urgentes se gestionan con heapq (O(log n))
- **Ordenamiento por prioridad y tiempo**: prioridad 0 es la más alta, desempate por orden de llegada

### Correcciones aplicadas (entregas anteriores)

- **Modularización**: archivos separados por clase según recomendación del profesor.
- **Recursividad implementada**: búsqueda y movimiento funcionan en toda la jerarquía de carpetas.
- **Tests unitarios**: 5 pruebas que validan recursividad, filtros, cola de urgentes y casos límite.
- **Casos límite documentados**: carpetas inexistentes, búsquedas vacías, filtros sin destino.

## Alcance de esta entrega

### Funcionalidades Implementadas

- ✅ Arquitectura modular en capas (src/)
- ✅ Algoritmos documentados con análisis de complejidad
- ✅ Servicios de alto nivel reutilizables
- ✅ Recursividad en búsqueda y movimiento
- ✅ Estructura de árbol de carpetas
- ✅ Cola de prioridad para urgentes (heapq)
- ✅ Filtros automáticos configurables
- ✅ Tests unitarios con pytest
- ✅ Documentación completa (README, MIGRACION, EJEMPLOS, ABSTRACT)

### Preparado para Extensión

- 🔄 Sistema de red de servidores (GestorRed con BFS)
- 🔄 Interfaz lista para GUI
- 🔄 Nuevos algoritmos fáciles de agregar

### Ver también

- [Guía de Migración](./MIGRACION.md) - Cómo migrar del código legacy
- [Ejemplos de Uso](./EJEMPLOS.md) - Uso de nuevos módulos
