"""
WSGI config for YqzyWeb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from os.path import dirname, abspath
import sys
PROJECT_DIR = dirname(dirname(abspath(__file__)))
if not PROJECT_DIR in sys.path:
    sys.path.insert(0, PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SelfieWeb.settings")

application = get_wsgi_application()
