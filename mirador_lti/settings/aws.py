from .base import *
from .secure import SECURE_SETTINGS

ALLOWED_HOSTS = ['.harvard.edu', 'localhost']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SECURE_SETTINGS.get('db_default_name', 'mirador_lti'),
        'USER': SECURE_SETTINGS.get('db_default_user', 'mirador_lti'),
        'PASSWORD': SECURE_SETTINGS.get('db_default_password'),
        'HOST': SECURE_SETTINGS.get('db_default_host', '127.0.0.1'),
        'PORT': SECURE_SETTINGS.get('db_default_port', 5432),
    } 
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECRET_KEY = SECURE_SETTINGS.get('django_secret_key')
LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('lti_oauth_credentials', {})
IIIF_IMAGE_SERVER_URL = SECURE_SETTINGS.get('iiif_image_server_url', 'http://localhost:8000/loris/')
AWS_KEY = SECURE_SETTINGS.get('aws_key')
AWS_SECRET = SECURE_SETTINGS.get('aws_secret')
S3_BUCKET = SECURE_SETTINGS.get('s3_bucket')
