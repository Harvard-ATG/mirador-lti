# to activate these settings, execute ./manage.py runserver --settings=mirador.settings.local
from .base import *

LTI_DEBUG = True
DEBUG = True
TEMPLATE_DEBUG = True

ENV_NAME = 'local'

# For Django Debug Toolbar:
INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)
DEBUG = SECURE_SETTINGS.get('enable_debug', True)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
