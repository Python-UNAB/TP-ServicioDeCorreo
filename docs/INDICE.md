# Índice de Documentación

Bienvenido a la documentación del Sistema de Correo Electrónico.

## 📚 Documentos Principales

### 1. [README.md](../readme.md)

**Descripción**: Documento principal del proyecto

- Introducción al proyecto
- Estructura del proyecto
- Objetivos y funcionalidades
- Diagramas UML
- Instrucciones de instalación y uso
- Análisis de complejidad

**Para**: Todos los usuarios, primera lectura

---

### 2. [abstract.md](./abstract.md)

**Descripción**: Decisiones de diseño y alcance

- Arquitectura del sistema
- Decisiones de diseño fundamentales
- Nueva arquitectura modular (refactorización)
- Análisis de cada capa (Models, Algorithms, Services, UI)
- Principios y patrones aplicados
- Tabla de complejidades

**Para**: Entender el diseño y la arquitectura

---

### 3. [MIGRACION.md](./MIGRACION.md)

**Descripción**: Guía de migración de app/ a src/

- Mapeo de archivos legacy a nueva estructura
- Descripción de nuevos módulos
- Cómo actualizar imports
- Instrucciones de ejecución
- Ventajas de la nueva estructura
- Estado del código legacy

**Para**: Desarrolladores migrando código existente

---

### 4. [EJEMPLOS.md](./EJEMPLOS.md)

**Descripción**: Ejemplos prácticos de uso

- Uso básico del sistema
- Ejemplos de algoritmos (búsqueda, ordenamiento, recorridos)
- Ejemplos de servicios (GestorMensajes, GestorCarpetas, GestorFiltros)
- GestorRed para sistema distribuido
- Flujo completo de ejemplo
- Integración con UI
- Testing con nuevos módulos

**Para**: Aprender a usar los nuevos módulos

---

### 5. [CONFIGURACION.md](./CONFIGURACION.md)

**Descripción**: Configuración del entorno de desarrollo

- Estructura de importaciones
- Configuración de debugging en VS Code
- Python Path
- Instalación de dependencias
- Ejecución de tests

**Para**: Setup del entorno de desarrollo

---

### 6. [RESUMEN_REFACTORIZACION.md](./RESUMEN_REFACTORIZACION.md)

**Descripción**: Resumen completo de la refactorización

- Tareas completadas
- Estadísticas del proyecto
- Objetivos cumplidos
- Estructura final completa
- Próximos pasos
- Beneficios de la nueva arquitectura

**Para**: Vista general de todos los cambios realizados

---

### 7. [ARQUITECTURA_VISUAL.md](./ARQUITECTURA_VISUAL.md)

**Descripción**: Visualización de la arquitectura con diagramas

- Arquitectura en capas con diagramas ASCII
- Flujo de datos (envío, búsqueda, filtros)
- Estructura de árbol de carpetas
- Recorrido BFS vs DFS visualizado
- Patrones de diseño con ejemplos
- Comparación de complejidades
- Dependencias entre módulos

**Para**: Entender visualmente la arquitectura y flujos

---

## 🗂️ Por Tema

### Arquitectura y Diseño

1. [abstract.md](./abstract.md) - Decisiones de diseño
2. [RESUMEN_REFACTORIZACION.md](./RESUMEN_REFACTORIZACION.md) - Resumen de cambios
3. [README.md](../readme.md) - Estructura del proyecto

### Desarrollo

1. [EJEMPLOS.md](./EJEMPLOS.md) - Cómo usar los módulos
2. [MIGRACION.md](./MIGRACION.md) - Migrar código legacy
3. [CONFIGURACION.md](./CONFIGURACION.md) - Setup del entorno

### Referencia Rápida

1. [README.md](../readme.md) - Instalación y uso
2. [requirements.txt](../requirements.txt) - Dependencias
3. [tests/](../tests/) - Tests unitarios

---

## 📖 Lectura Recomendada por Rol

### 👨‍💻 Desarrollador Nuevo

1. README.md - Entender qué hace el proyecto
2. abstract.md - Conocer la arquitectura
3. EJEMPLOS.md - Aprender a usar los módulos
4. CONFIGURACION.md - Configurar el entorno

### 🔧 Mantenedor del Proyecto

1. RESUMEN_REFACTORIZACION.md - Ver todos los cambios
2. MIGRACION.md - Entender la migración
3. abstract.md - Revisar decisiones de diseño
4. EJEMPLOS.md - Referencia de uso

### 🎓 Estudiante/Evaluador

1. README.md - Visión general
2. abstract.md - Decisiones y complejidad
3. RESUMEN_REFACTORIZACION.md - Alcance de la entrega
4. Código en src/ - Implementación

### 🚀 Usuario Final

1. README.md - Cómo instalar y usar
2. Manual de uso en README
3. CONFIGURACION.md - Si hay problemas

---

## 📊 Documentos por Tamaño

| Documento                  | Páginas aprox. | Tiempo lectura |
| -------------------------- | -------------- | -------------- |
| README.md                  | 6-8            | 15-20 min      |
| abstract.md                | 3-4            | 10 min         |
| MIGRACION.md               | 3              | 8 min          |
| EJEMPLOS.md                | 5              | 12 min         |
| CONFIGURACION.md           | 1              | 3 min          |
| RESUMEN_REFACTORIZACION.md | 4              | 10 min         |

**Total**: ~25 páginas, ~1 hora de lectura completa

---

## 🔍 Búsqueda Rápida

### "¿Cómo ejecuto el proyecto?"

→ [README.md - Cómo probar rápidamente](../readme.md#cómo-probar-rápidamente)

### "¿Cómo uso los nuevos servicios?"

→ [EJEMPLOS.md - Usando los Servicios](./EJEMPLOS.md#usando-los-servicios)

### "¿Qué cambió en esta entrega?"

→ [RESUMEN_REFACTORIZACION.md](./RESUMEN_REFACTORIZACION.md)

### "¿Por qué se diseñó así?"

→ [abstract.md - Decisiones de diseño](./abstract.md#decisiones-de-diseño)

### "¿Cómo migro mi código?"

→ [MIGRACION.md](./MIGRACION.md)

### "¿Cómo configuro VS Code?"

→ [CONFIGURACION.md](./CONFIGURACION.md)

### "¿Cuál es la complejidad de X?"

→ [abstract.md - Análisis de Complejidad](./abstract.md) o [README.md - Complejidad](../readme.md#complejidad-y-eficiencia)

---

## 📁 Estructura de Documentación

```
docs/
├── INDICE.md                      # Este archivo
├── abstract.md                    # Diseño y arquitectura
├── MIGRACION.md                   # Guía de migración
├── EJEMPLOS.md                    # Ejemplos de código
├── CONFIGURACION.md               # Setup de desarrollo
└── RESUMEN_REFACTORIZACION.md     # Resumen de cambios
```

---

## ✨ Sugerencias de Lectura

**Primera vez con el proyecto:**

1. README.md (secciones: Objetivos, Estructura, Cómo probar)
2. abstract.md (sección: Arquitectura general)
3. EJEMPLOS.md (Uso Básico del Sistema)

**Quiero desarrollar nueva funcionalidad:**

1. abstract.md (Arquitectura completa)
2. EJEMPLOS.md (Ejemplos de uso de servicios)
3. Código fuente en src/

**Estoy evaluando el proyecto:**

1. README.md (completo)
2. abstract.md (completo)
3. RESUMEN_REFACTORIZACION.md
4. Tests y código fuente

---

**Última actualización**: Esta documentación refleja la refactorización completa a arquitectura modular en `src/`.
