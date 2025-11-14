# Configuración de VS Code para Python

Este proyecto está organizado como un paquete Python modular.

## Estructura de Importaciones

El proyecto tiene dos formas de ejecutarse:

### 1. Como script directo (Recomendado)

```bash
python main.py
```

### 2. Como módulo Python

```bash
python -m src.ui.cli
```

## Configuración para Debugging

Agregar al `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Main",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

## Python Path

El proyecto no requiere modificación del PYTHONPATH si se ejecuta desde la raíz.

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

O solo pytest para desarrollo:

```bash
pip install pytest
```

## Tests

Ejecutar todos los tests:

```bash
pytest
```

Ejecutar con verbose:

```bash
pytest -v
```

Ejecutar un test específico:

```bash
pytest tests/test_correo.py::test_busqueda_recursiva_mensajes
```
