from django.conf.urls import url
from .views import manifest
urlpatterns = [
    url(r'^([^/]*)/manifest.json$', manifest, name='manifest')
]
