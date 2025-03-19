"""
WSGI config for dynamics project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dynamics.settings')

application = get_wsgi_application()



# Set Cloudinary environment variables BEFORE importing Django
os.environ['CLOUDINARY_CLOUD_NAME'] = 'intitulado'
os.environ['CLOUDINARY_API_KEY'] = '241739348942567'
os.environ['CLOUDINARY_API_SECRET'] = 'wWcQab-9C_R0poTu8p5aOaAhvSk'
os.environ['CLOUDINARY_URL'] = 'cloudinary://241739348942567:wWcQab-9C_R0poTu8p5aOaAhvSk@intitulado'

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dynamics.settings')

application = get_wsgi_application()

