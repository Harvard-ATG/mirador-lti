from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from .views import index
import os

urlpatterns = [
    url(r'^(?P<course_id>\d+)$', index, name='index'),
    url(r'^images/logos/(?P<path>.*)$', serve, { 
        'document_root': os.path.join(settings.STATIC_ROOT, 'images', 'logos')
    }),
]
