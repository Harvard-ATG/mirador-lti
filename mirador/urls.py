from django.conf.urls import url
from .views import index
urlpatterns = [
    url(r'^(?P<course_id>\d+)$', index, name='index')
]
