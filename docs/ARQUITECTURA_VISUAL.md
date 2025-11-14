# Visualización de la Arquitectura

## 🏗️ Arquitectura en Capas

```
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                  │
│                                                          │
│  ┌────────────────┐          ┌─────────────────┐       │
│  │  MenuPrincipal │          │   MenuUsuario    │       │
│  │   (cli.py)     │          │    (menu.py)     │       │
│  └────────┬───────┘          └────────┬────────┘       │
│           │                           │                 │
└───────────┼───────────────────────────┼─────────────────┘
            │                           │
            ▼                           ▼
┌─────────────────────────────────────────────────────────┐
│                  CAPA DE SERVICIOS                       │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Gestor     │  │   Gestor     │  │   Gestor     │ │
│  │  Mensajes    │  │  Carpetas    │  │   Filtros    │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                  │          │
│         │    ┌────────────┴──────────┐       │          │
│         │    │    GestorRed (BFS)    │       │          │
│         │    └───────────────────────┘       │          │
└─────────┼─────────────┼──────────────────────┼──────────┘
          │             │                      │
          ▼             ▼                      ▼
┌─────────────────────────────────────────────────────────┐
│                   CAPA DE ALGORITMOS                     │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Búsqueda   │  │ Ordenamiento │  │  Recorridos  │ │
│  │  Recursiva   │  │   Timsort    │  │   BFS/DFS    │ │
│  │    O(n)      │  │  O(n log n)  │  │    O(n)      │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│                   CAPA DE MODELOS                        │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Usuario    │  │   Mensaje    │  │   Carpeta    │ │
│  │              │  │              │  │   (Árbol)    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│           ┌──────────────────────────┐                  │
│           │   ServidorCorreo         │                  │
│           │   (Coordinador)          │                  │
│           └──────────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

## 📊 Flujo de Datos

### Envío de Mensaje

```
Usuario (CLI)
    │
    ├─► MenuUsuario.procesar_opcion("1")
    │       │
    │       ├─► GestorMensajes.enviar()
    │       │       │
    │       │       ├─► ServidorCorreo.enviar_mensaje()
    │       │       │       │
    │       │       │       ├─► Mensaje() [crear]
    │       │       │       │
    │       │       │       ├─► Usuario.aplicar_filtros()
    │       │       │       │       │
    │       │       │       │       └─► Carpeta.agregar_mensaje()
    │       │       │       │
    │       │       │       └─► heapq.heappush() [si urgente]
    │       │       │
    │       │       └─► return Mensaje
    │       │
    │       └─► "Mensaje enviado"
    │
    └─► Mostrar confirmación
```

### Búsqueda Recursiva

```
Usuario quiere buscar "proyecto"
    │
    ├─► MenuUsuario.procesar_opcion("3")
    │       │
    │       ├─► Usuario.buscar_mensajes(criterio)
    │       │       │
    │       │       ├─► for each Carpeta:
    │       │       │   │
    │       │       │   ├─► Carpeta.buscar_mensajes(criterio)
    │       │       │   │       │
    │       │       │   │       ├─► [m for m in mensajes if criterio(m)]
    │       │       │   │       │
    │       │       │   │       └─► for each Subcarpeta:
    │       │       │   │               │
    │       │       │   │               └─► Subcarpeta.buscar_mensajes() [RECURSIÓN]
    │       │       │   │
    │       │       │   └─► Acumular resultados
    │       │       │
    │       │       └─► return Lista[Mensaje]
    │       │
    │       └─► Mostrar resultados
    │
    └─► Ver mensajes encontrados
```

### Aplicación de Filtros

```
Nuevo mensaje llega a Entrada
    │
    ├─► ServidorCorreo.enviar_mensaje()
    │       │
    │       ├─► Usuario.aplicar_filtros(mensaje)
    │       │       │
    │       │       ├─► for each filtro in filtros:
    │       │       │   │
    │       │       │   ├─► if filtro["condicion"](mensaje):
    │       │       │   │   │
    │       │       │   │   ├─► Carpeta.eliminar_mensaje(mensaje)
    │       │       │   │   │
    │       │       │   │   ├─► CarpetaDestino.agregar_mensaje(mensaje)
    │       │       │   │   │
    │       │       │   │   └─► return filtro["nombre"]
    │       │       │   │
    │       │       │   └─► continue [si no coincide]
    │       │       │
    │       │       └─► return None [si ningún filtro coincide]
    │       │
    │       └─► Mensaje en carpeta correcta
    │
    └─► Finalizado
```

## 🌳 Estructura de Árbol de Carpetas

```
Usuario.carpetas (Dict)
    │
    ├─► "Entrada" ──► Carpeta
    │                     │
    │                     ├─► mensajes: List[Mensaje]
    │                     │
    │                     └─► subcarpetas: Dict
    │                             │
    │                             ├─► "Proyectos" ──► Carpeta
    │                             │                       │
    │                             │                       ├─► mensajes: []
    │                             │                       │
    │                             │                       └─► subcarpetas:
    │                             │                               │
    │                             │                               └─► "2025" ──► Carpeta
    │                             │                                                 │
    │                             │                                                 └─► mensajes: [msg1, msg2]
    │                             │
    │                             └─► "Personal" ──► Carpeta
    │                                                   │
    │                                                   └─► mensajes: [msg3]
    │
    └─► "Enviados" ──► Carpeta
                          │
                          └─► mensajes: [msg4, msg5, msg6]
```

## 🔄 Recorrido BFS vs DFS

### BFS (Breadth-First Search)

```
Carpeta Raíz: "Entrada"
    │
    ├─ Nivel 1: ["Entrada"]
    │
    ├─ Nivel 2: ["Entrada/Proyectos", "Entrada/Personal"]
    │
    └─ Nivel 3: ["Entrada/Proyectos/2025"]

Orden de visita:
Entrada → Entrada/Proyectos → Entrada/Personal → Entrada/Proyectos/2025
```

### DFS (Depth-First Search)

```
Carpeta Raíz: "Entrada"
    │
    ├─ Entrada
    │   │
    │   ├─ Entrada/Proyectos
    │   │   │
    │   │   └─ Entrada/Proyectos/2025
    │   │
    │   └─ Entrada/Personal

Orden de visita:
Entrada → Entrada/Proyectos → Entrada/Proyectos/2025 → Entrada/Personal
```

## 🎯 Patrones de Diseño Visualizados

### Factory Pattern (GestorFiltros)

```
GestorFiltros (Factory)
    │
    ├─► crear_filtro_asunto(palabra) ──► lambda mensaje: palabra in mensaje.asunto
    │
    ├─► crear_filtro_remitente(user) ──► lambda mensaje: mensaje.remitente == user
    │
    └─► crear_filtro_urgente() ──────► lambda mensaje: mensaje.es_urgente


Usuario utiliza:
    filtro = GestorFiltros.crear_filtro_asunto("proyecto")
    usuario.agregar_filtro("Proyectos", filtro, "Trabajo/Proyectos")
```

### Composite Pattern (Carpeta)

```
Carpeta (Component)
    ├── mensajes: List[Mensaje] (Leaf)
    └── subcarpetas: Dict[str, Carpeta] (Composite)
            │
            └── Cada subcarpeta es también una Carpeta (recursión)

Operaciones recursivas:
    - buscar_mensajes() recorre todo el árbol
    - extraer_mensajes() modifica todo el árbol
    - recorrer() genera todo el árbol
```

### Facade Pattern (Servicios)

```
Usuario de alto nivel
    │
    └─► GestorMensajes (Facade)
            │
            ├─► ServidorCorreo.enviar_mensaje()
            ├─► Usuario.buscar_mensajes()
            ├─► Usuario.mover_mensajes()
            └─► ServidorCorreo.extraer_mensaje_urgente()

Simplifica operaciones complejas detrás de una interfaz simple
```

## 📈 Comparación de Complejidad

### Búsqueda de Mensaje

| Método                 | Complejidad | Mejor Caso | Peor Caso |
| ---------------------- | ----------- | ---------- | --------- |
| Búsqueda lineal        | O(n)        | O(1)       | O(n)      |
| Por carpeta específica | O(m)        | O(1)       | O(m)      |
| Recursiva en árbol     | O(n)        | O(1)       | O(n)      |

Donde: n = total mensajes, m = mensajes en una carpeta

### Ordenamiento

| Algoritmo        | Complejidad | Estable | In-place |
| ---------------- | ----------- | ------- | -------- |
| Timsort (Python) | O(n log n)  | Sí      | No       |
| Por fecha        | O(n log n)  | Sí      | No       |
| Por prioridad    | O(n log n)  | Sí      | No       |

### Recorrido de Carpetas

| Método        | Tiempo | Espacio | Uso             |
| ------------- | ------ | ------- | --------------- |
| BFS           | O(n)   | O(w)    | Nivel por nivel |
| DFS recursivo | O(n)   | O(h)    | Profundidad     |
| DFS iterativo | O(n)   | O(h)    | Sin recursión   |

Donde: n = carpetas, w = ancho máximo, h = altura

## 🔗 Dependencias entre Módulos

```
┌──────────┐
│    UI    │
└────┬─────┘
     │ depende de
     ▼
┌──────────┐
│ Services │
└────┬─────┘
     │ depende de
     ├────────┬─────────┐
     ▼        ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Models │ │ Algos  │ │ Models │
└────────┘ └────────┘ └────────┘

Regla: Las capas superiores dependen de las inferiores, nunca al revés
```

## 🚀 Extensibilidad

### Agregar Nueva Funcionalidad

```
Nueva funcionalidad: "Archivar mensajes antiguos"

1. Algoritmo (src/algorithms/):
   ├─► crear archivo_automatico.py
   └─► def archivar_por_fecha(carpeta, dias): ...

2. Servicio (src/services/):
   ├─► agregar a GestorMensajes o crear GestorArchivo
   └─► def archivar_antiguos(usuario, dias): ...

3. UI (src/ui/):
   ├─► agregar opción en MenuUsuario
   └─► "9. Archivar mensajes antiguos"

No requiere modificar código existente ✅
```

---

Este diagrama visual ayuda a entender la arquitectura y el flujo de datos del sistema.
