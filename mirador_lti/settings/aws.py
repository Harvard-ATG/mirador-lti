from .base import *
from .secure import SECURE_SETTINGS

ALLOWED_HOSTS = ['.harvard.edu', 'localhost']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECRET_KEY = SECURE_SETTINGS.get('django_secret_key')
LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('lti_oauth_credentials', {})
IIIF_IMAGE_SERVER_URL = SECURE_SETTINGS.get('iiif_image_server_url', 'http://localhost:8000/loris/')