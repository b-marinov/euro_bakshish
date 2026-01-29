"""
ASGI config for euro_bakshish project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'euro_bakshish.settings')

application = get_asgi_application()
