import os
import dj_database_url
import json
import dotenv
from .base import *

dotenv.read_dotenv(os.path.join(BASE_DIR, '.env'))

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Parse database configuration from $DATABASE_URL
DATABASES = {}
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
LTI_OAUTH_CREDENTIALS = json.loads(os.environ.get('LTI_OAUTH_CREDENTIALS'))
IIIF_IMAGE_SERVER_URL = os.environ.get('IIIF_IMAGE_SERVER_URL')
AWS_KEY = os.environ.get('AWS_KEY')
AWS_SECRET = os.environ.get('AWS_SECRET')
S3_BUCKET = os.environ.get('S3_BUCKET')