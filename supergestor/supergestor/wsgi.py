# coding: utf-8

"""
Configuración WSGI para proyecto supergestor.
La implementación WSGI es una aplicación que puede llamar al servidor de aplicaciones,
para comunicarse con el código.
Obtiene la ruta de la aplicación que puede llamar desde su configuración.
La línea os.environ.setdefault establece el módulo de configuración predeterminada para usar, 
supergestor.settings es el nombre del paquete de proyecto.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supergestor.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
