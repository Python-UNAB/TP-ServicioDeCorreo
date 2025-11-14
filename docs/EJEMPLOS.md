# Ejemplos de Uso - Nueva Arquitectura

Este documento muestra cómo usar los nuevos módulos del sistema.

## Uso Básico del Sistema

### Inicializar el Servidor

```python
from src.models import ServidorCorreo

servidor = ServidorCorreo()
servidor.registrar_usuario("alice", "password123")
servidor.registrar_usuario("bob", "password456")
```

## Usando los Algoritmos

### Búsqueda Recursiva

```python
from src.algorithms import buscar_por_asunto, buscar_por_remitente

# Obtener la carpeta de un usuario
usuario = servidor.obtener_usuario("alice")
carpeta_entrada = usuario.obtener_carpeta("Entrada")

# Buscar mensajes por asunto
mensajes = buscar_por_asunto(carpeta_entrada, "proyecto")

# Buscar por remitente
mensajes_bob = buscar_por_remitente(carpeta_entrada, "bob")
```

### Ordenamiento de Mensajes

```python
from src.algorithms import ordenar_por_fecha, ordenar_por_prioridad

# Obtener mensajes
mensajes = carpeta_entrada.listar_mensajes()

# Ordenar por fecha (más recientes primero)
mensajes_ordenados = ordenar_por_fecha(mensajes, descendente=True)

# Ordenar por prioridad
mensajes_urgentes = ordenar_por_prioridad(mensajes, descendente=True)
```

### Recorrido de Carpetas (BFS/DFS)

```python
from src.algorithms import recorrer_carpetas_bfs, recorrer_carpetas_dfs

# Recorrido en anchura
carpetas_bfs = recorrer_carpetas_bfs(carpeta_entrada)
for ruta, carpeta in carpetas_bfs:
    print(f"{ruta}: {len(carpeta.listar_mensajes())} mensajes")

# Recorrido en profundidad
carpetas_dfs = recorrer_carpetas_dfs(carpeta_entrada)
```

## Usando los Servicios

### GestorMensajes - Operaciones de Alto Nivel

```python
from src.services import GestorMensajes

gestor = GestorMensajes(servidor)

# Enviar mensaje con prioridad
gestor.enviar("alice", "bob", "Reunión urgente", "Mañana a las 10",
              urgente=True, prioridad=0)

# Buscar mensajes de un usuario
mensajes = gestor.buscar_mensajes_usuario(
    "alice",
    lambda m: "proyecto" in m.mostrar_asunto.lower()
)

# Mover mensajes
movidos = gestor.mover_mensajes_usuario(
    "alice",
    lambda m: "trabajo" in m.mostrar_asunto.lower(),
    "Trabajo/Proyectos",
    crear_destino=True
)
print(f"Se movieron {movidos} mensajes")

# Obtener todos los urgentes pendientes
urgentes = gestor.obtener_mensajes_urgentes()
```

### GestorCarpetas - Gestión de Estructura

```python
from src.services import GestorCarpetas

gestor_carpetas = GestorCarpetas()

usuario = servidor.obtener_usuario("alice")

# Crear estructura de carpetas
gestor_carpetas.crear_carpeta(usuario, "Trabajo/Proyectos/2025")
gestor_carpetas.crear_carpeta(usuario, "Personal/Familia")

# Listar todas las carpetas
carpetas = gestor_carpetas.listar_carpetas(usuario)
for carpeta in carpetas:
    print(f"- {carpeta}")

# Obtener estadísticas de una carpeta
entrada = usuario.obtener_carpeta("Entrada")
stats = gestor_carpetas.obtener_estadisticas_carpeta(entrada)
print(f"Mensajes directos: {stats['mensajes_directos']}")
print(f"Mensajes totales: {stats['mensajes_totales']}")
print(f"Subcarpetas: {stats['subcarpetas_directas']}")

# Recorrer estructura completa
estructura = gestor_carpetas.recorrer_estructura(usuario)
for ruta, carpeta in estructura:
    print(f"{ruta}: {carpeta.nombre}")
```

### GestorFiltros - Automatización de Clasificación

```python
from src.services import GestorFiltros

# Crear filtros predefinidos
filtro_proyecto = GestorFiltros.crear_filtro_asunto("proyecto")
filtro_bob = GestorFiltros.crear_filtro_remitente("bob")
filtro_urgentes = GestorFiltros.crear_filtro_urgente()

# Agregar filtros a un usuario
usuario = servidor.obtener_usuario("alice")

GestorFiltros.agregar_filtro_usuario(
    usuario,
    "Proyectos",
    filtro_proyecto,
    "Trabajo/Proyectos",
    crear_destino=True
)

GestorFiltros.agregar_filtro_usuario(
    usuario,
    "De Bob",
    filtro_bob,
    "Personal/Bob"
)

GestorFiltros.agregar_filtro_usuario(
    usuario,
    "Urgentes",
    filtro_urgentes,
    "Urgentes"
)

# Listar filtros
filtros = GestorFiltros.listar_filtros_usuario(usuario)
print("Filtros activos:", filtros)

# Quitar un filtro
GestorFiltros.quitar_filtro_usuario(usuario, "De Bob")
```

### GestorRed - Red de Servidores (Preparado para Futuro)

```python
from src.services.gestor_red import GestorRed
from src.models import ServidorCorreo

# Crear red de servidores
red = GestorRed()

# Registrar servidores
servidor_mx = ServidorCorreo()
servidor_ar = ServidorCorreo()
servidor_br = ServidorCorreo()

red.registrar_servidor("servidor.mx", servidor_mx)
red.registrar_servidor("servidor.ar", servidor_ar)
red.registrar_servidor("servidor.br", servidor_br)

# Conectar servidores
red.conectar_servidores("servidor.mx", "servidor.ar")
red.conectar_servidores("servidor.ar", "servidor.br")

# Encontrar ruta entre servidores (BFS)
ruta = red.encontrar_ruta("servidor.mx", "servidor.br")
print(f"Ruta: {' -> '.join(ruta)}")
# Output: Ruta: servidor.mx -> servidor.ar -> servidor.br

# Listar todos los dominios
dominios = red.listar_dominios()
print("Servidores en la red:", dominios)
```

## Flujo Completo de Ejemplo

```python
from src.models import ServidorCorreo
from src.services import GestorMensajes, GestorCarpetas, GestorFiltros
from src.algorithms import ordenar_por_fecha

# 1. Inicializar sistema
servidor = ServidorCorreo()
servidor.registrar_usuario("alice", "pass123")
servidor.registrar_usuario("bob", "pass456")

# 2. Configurar estructura de carpetas
gestor_carpetas = GestorCarpetas()
alice = servidor.obtener_usuario("alice")
gestor_carpetas.crear_carpeta(alice, "Trabajo/Proyectos")
gestor_carpetas.crear_carpeta(alice, "Personal")

# 3. Configurar filtros automáticos
GestorFiltros.agregar_filtro_usuario(
    alice,
    "Trabajo",
    lambda m: "trabajo" in m.mostrar_asunto.lower(),
    "Trabajo"
)

# 4. Enviar mensajes
gestor_msg = GestorMensajes(servidor)
gestor_msg.enviar("bob", "alice", "Proyecto Final", "Contenido del proyecto")
gestor_msg.enviar("bob", "alice", "Trabajo urgente", "Revisar ASAP",
                  urgente=True, prioridad=0)

# 5. Los filtros se aplican automáticamente
# El mensaje "Trabajo urgente" se mueve a la carpeta "Trabajo"

# 6. Buscar y organizar
trabajo = alice.obtener_carpeta("Trabajo")
mensajes = trabajo.listar_mensajes()
mensajes_ordenados = ordenar_por_fecha(mensajes)

for msg in mensajes_ordenados:
    print(msg.mostrar_resumen())

# 7. Obtener estadísticas
stats = gestor_carpetas.obtener_estadisticas_carpeta(trabajo)
print(f"Total de mensajes de trabajo: {stats['mensajes_totales']}")
```

## Integración con la UI

Los menús ya utilizan estos servicios internamente. Para crear una interfaz personalizada:

```python
from src.ui import MenuPrincipal, MenuUsuario
from src.models import ServidorCorreo

# Crear servidor
servidor = ServidorCorreo()

# Usar menú principal
menu = MenuPrincipal(servidor)
menu.mostrar()
continuar, usuario = menu.procesar_opcion("2")  # Registrar

# Si usuario autenticado, usar menú de usuario
if usuario:
    menu_usuario = MenuUsuario(servidor, usuario)
    menu_usuario.mostrar()
    menu_usuario.procesar_opcion("1")  # Enviar mensaje
```

## Testing con los Nuevos Módulos

```python
import pytest
from src.models import ServidorCorreo
from src.services import GestorMensajes
from src.algorithms import buscar_por_asunto

def test_flujo_completo():
    servidor = ServidorCorreo()
    servidor.registrar_usuario("test1", "pass")
    servidor.registrar_usuario("test2", "pass")

    gestor = GestorMensajes(servidor)
    gestor.enviar("test1", "test2", "Test", "Contenido")

    usuario = servidor.obtener_usuario("test2")
    entrada = usuario.obtener_carpeta("Entrada")

    mensajes = buscar_por_asunto(entrada, "Test")
    assert len(mensajes) == 1
    assert mensajes[0].mostrar_asunto == "Test"
```
