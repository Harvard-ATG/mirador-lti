# to activate these settings, execute ./manage.py runserver --settings=mirador.settings.local
from .base import *

ALLOWED_HOSTS = ['localhost']


SECRET_KEY = SECURE_SETTINGS.get('django_secret_key')
LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('lti_oauth_credentials', {})
IIIF_IMAGE_SERVER_URL = SECURE_SETTINGS.get('iiif_image_server_url', 'http://localhost:8000/loris/')