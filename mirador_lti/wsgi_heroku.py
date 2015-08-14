"""
WSGI config.
It exposes the WSGI callable as a module-level variable named ``application``.
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirador_lti.settings.heroku")
application = Cling(get_wsgi_application())

