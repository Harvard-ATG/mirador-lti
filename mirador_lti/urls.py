from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lti/', include('django_app_lti.urls', namespace="lti")),
    url(r'^iiif/', include('iiif.urls', namespace="iiif")),
    url(r'^mirador/', include('mirador.urls', namespace="mirador")),
]



