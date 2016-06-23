from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^endpointnotfound/$', views.noendpoint, name='noendpoint'),
    url(r'^keystone_malfunctioned/$', views.keystonegone, name='keystonegone'),
]
