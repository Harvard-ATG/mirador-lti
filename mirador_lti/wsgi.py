"""
WSGI config for skeleton project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

if os.environ.get("DJANGO_SETTINGS_MODULE", None) == "mirador_lti.settings.heroku":
    application = Cling(get_wsgi_application())
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirador_lti.settings.aws")
    application = get_wsgi_application()

