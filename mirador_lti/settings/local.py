# to activate these settings, execute ./manage.py runserver --settings=mirador.settings.local
from .base import *
from .secure import SECURE_SETTINGS

ALLOWED_HOSTS = ['localhost']

SECRET_KEY = SECURE_SETTINGS.get('django_secret_key')
LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('lti_oauth_credentials', {})
IIIF_IMAGE_SERVER_URL = SECURE_SETTINGS.get('iiif_image_server_url', 'http://localhost:8000/loris/')
AWS_KEY = SECURE_SETTINGS.get('aws_key')
AWS_SECRET = SECURE_SETTINGS.get('aws_secret')
S3_BUCKET = SECURE_SETTINGS.get('s3_bucket')