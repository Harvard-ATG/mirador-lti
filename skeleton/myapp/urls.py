from django.conf.urls import url
urlpatterns = [
    url(r'^$', 'myapp.views.index', name='index'),
    url(r'^course/(?P<course_id>\d+)$', 'myapp.views.index', name='index'),
]
