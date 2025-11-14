# Guía de Migración: app/ → src/

## Resumen de Cambios

El proyecto ha sido completamente refactorizado de una estructura plana en `app/` a una arquitectura modular en `src/` con clara separación de responsabilidades.

## Mapeo de Archivos

### Código Legacy → Nueva Estructura

| Archivo Legacy    | Nueva Ubicación                    | Notas                         |
| ----------------- | ---------------------------------- | ----------------------------- |
| `app/usuario.py`  | `src/models/usuario.py`            | Sin cambios en lógica         |
| `app/mensaje.py`  | `src/models/mensaje.py`            | Sin cambios en lógica         |
| `app/carpeta.py`  | `src/models/carpeta.py`            | Sin cambios en lógica         |
| `app/servidor.py` | `src/models/servidor_correo.py`    | Renombrado a `ServidorCorreo` |
| `app/main.py`     | `src/ui/cli.py` + `src/ui/menu.py` | Dividido en módulos           |
| -                 | `main.py` (raíz)                   | Nuevo punto de entrada        |

### Nuevos Módulos Agregados

#### `src/algorithms/` - Algoritmos con Análisis de Complejidad

- **busqueda_recursiva.py**: Funciones helper para búsqueda en carpetas

  - `buscar_en_carpetas()` - O(n)
  - `buscar_por_remitente()` - O(n)
  - `buscar_por_asunto()` - O(n\*m)

- **ordenamiento.py**: Algoritmos de ordenamiento de mensajes

  - `ordenar_por_fecha()` - O(n log n)
  - `ordenar_por_prioridad()` - O(n log n)
  - `ordenar_por_remitente()` - O(n log n)

- **recorrido_grafo.py**: Recorridos BFS/DFS
  - `recorrer_carpetas_bfs()` - O(n), espacio O(w)
  - `recorrer_carpetas_dfs()` - O(n), espacio O(h)
  - `recorrer_carpetas_dfs_iterativo()` - O(n), espacio O(h)

#### `src/services/` - Capa de Lógica de Negocio

- **gestor_mensajes.py**: Operaciones de alto nivel con mensajes

  - `enviar()`, `buscar_mensajes_usuario()`, `mover_mensajes_usuario()`, `obtener_mensajes_urgentes()`

- **gestor_carpetas.py**: Gestión de carpetas

  - `crear_carpeta()`, `listar_carpetas()`, `obtener_estadisticas_carpeta()`, `recorrer_estructura()`

- **gestor_filtros.py**: Manejo de filtros automáticos

  - `crear_filtro_asunto()`, `crear_filtro_remitente()`, `crear_filtro_urgente()`
  - `agregar_filtro_usuario()`, `quitar_filtro_usuario()`, `listar_filtros_usuario()`

- **gestor_red.py**: Base para red de servidores (futuras extensiones)
  - `registrar_servidor()`, `conectar_servidores()`, `encontrar_ruta()` con BFS

#### `src/ui/` - Interfaz Modular

- **cli.py**: Punto de entrada CLI

  - `ejecutar_cli()`, `ejecutar_menu_usuario()`

- **menu.py**: Clases de menú separadas
  - `MenuPrincipal`: Maneja autenticación y opciones del servidor
  - `MenuUsuario`: Maneja todas las operaciones del usuario autenticado

## Cómo Actualizar las Importaciones

### Antes (app/)

```python
from app.servidor import ServidorCorreo
from app.usuario import Usuario
from app.mensaje import Mensaje
from app.carpeta import Carpeta
```

### Ahora (src/)

```python
from src.models import ServidorCorreo, Usuario, Mensaje, Carpeta
# O importaciones específicas:
from src.models.servidor_correo import ServidorCorreo
from src.models.usuario import Usuario
```

### Para Tests

```python
# Antes
from app.mensaje import Mensaje
from app.servidor import ServidorCorreo
from app.usuario import Usuario

# Ahora
from src.models.mensaje import Mensaje
from src.models.servidor_correo import ServidorCorreo
from src.models.usuario import Usuario
```

## Cómo Ejecutar

### Antes

```bash
python -m app.main
```

### Ahora

```bash
# Opción 1 (recomendada): Usar el punto de entrada principal
python main.py

# Opción 2: Ejecutar como módulo
python -m src.ui.cli
```

## Ventajas de la Nueva Estructura

1. **Separación de responsabilidades**: Cada capa tiene un propósito claro
2. **Testabilidad mejorada**: Los servicios y algoritmos son fáciles de testear aisladamente
3. **Extensibilidad**: Fácil agregar nuevos algoritmos o servicios sin afectar el resto
4. **Documentación**: Cada algoritmo tiene su complejidad documentada
5. **Escalabilidad**: Preparado para funcionalidades futuras (red de servidores, GUI)
6. **Mantenibilidad**: Código más limpio y organizado

## Estado del Código Legacy

La carpeta `app/` se mantiene por compatibilidad pero está **deprecada**. Todo el desarrollo futuro debe hacerse en `src/`.

## Testing

Los tests se actualizaron para usar las nuevas importaciones:

```bash
pytest -q
```

## Próximos Pasos Recomendados

1. ✅ Validar que el nuevo sistema funciona correctamente
2. ✅ Ejecutar todos los tests y verificar que pasan
3. 🔄 Migrar cualquier código custom de `app/` a `src/`
4. 🔄 Eliminar `app/` cuando se confirme que todo funciona
5. ➕ Agregar más tests para los nuevos módulos
6. ➕ Implementar GUI con tkinter usando la capa de servicios
