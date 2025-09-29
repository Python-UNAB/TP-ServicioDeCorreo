# Abstract

Decisiones de diseño:

- ServidorCorreo centraliza registro/autenticación y el enrutamiento de mensajes entre usuarios.
- Usuario posee carpetas predefinidas (Entrada, Enviados) para simplificar el flujo básico.
- Mensaje es inmutable en sus metadatos luego de creado; solo se muestra o resume.
- Modularización por archivos: cada clase en su módulo, más `app/main.py` como punto de entrada.

Alcance de esta entrega:

- Implementación en memoria sin persistencia.
- Funcionalidades básicas de consola para registrar, autenticar y visualizar correos.
- Base lista para extender con validaciones, persistencia y filtros.
