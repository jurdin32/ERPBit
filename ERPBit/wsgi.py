"""
WSGI config for ERPBit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ERPBit.settings")

application = get_wsgi_application()

print("LA INSTANCIA CAMBIO A CELERY APPS")
print('Ejecutar en nueva consola: celery -A  ERPBit flower')
print('Efecutar en otra consola: python manage.py celeryd -l info')