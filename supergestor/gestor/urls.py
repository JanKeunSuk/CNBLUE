from django.conf.urls import patterns, url

from gestor import views

urlpatterns = patterns('',
    url(r'^hola/$', views.holaView, name='hola'),
    url(r'^registrar/', views.registrarUsuarioView, name='nuevo_usuario'),
    url(r'^save/', views.guardarUsuarioView, name='guardar_nuevo_usuario'),
)
