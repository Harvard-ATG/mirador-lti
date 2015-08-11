from django.conf.urls import url
from .views import manifest
urlpatterns = [
    url(r'^(?P<manifest_id>[0-9:]+)/(?P<object_type>manifest).json$', manifest, name='manifest'),
    url(r'^(?P<manifest_id>[0-9:]+)/(?P<object_type>sequence)/(?P<object_id>\d+).json$', manifest, name='sequence'),
    url(r'^(?P<manifest_id>[0-9:]+)/(?P<object_type>canvas)/(?P<object_id>\d+).json$', manifest, name='canvas'),
    url(r'^(?P<manifest_id>[0-9:]+)/(?P<object_type>resource)/(?P<object_id>\d+).json$', manifest, name='resource'),
]
