from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from .views import index, import_api_load, import_api_assign
import os

urlpatterns = [
    url(r'^(?P<resource_id>\d+)$', index, name='index'),
    url(r'^images/logos/(?P<path>.*)$', serve, { 
        'document_root': os.path.join(settings.STATIC_ROOT, 'images', 'logos')
    }),
    url(r'^importapi/load$', import_api_load, name="import-load"),
    url(r'^importapi/assign$', import_api_assign, name="import-assign"),
]
