"""
WSGI config for euro_bakshish project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'euro_bakshish.settings')

application = get_wsgi_application()
