from django.conf.urls import url
from .views import manifest
urlpatterns = [
    url(r'^(\d+)/manifest.json$', manifest, name='manifest'),
    url(r'^(\d+)/(sequence)/(\d+).json$', manifest, name='sequence'),
    url(r'^(\d+)/(canvas)/(\d+).json$', manifest, name='canvas'),
    url(r'^(\d+)/(resource)/(\d+).json$', manifest, name='resource'),
]
