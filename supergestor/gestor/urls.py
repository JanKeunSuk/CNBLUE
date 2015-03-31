
"""Archivo donde se especifican las expresiones regulares que seran filtradas y 
y redirigidas a una vista para el procesamiento de las peticiiones. El funcionamiento 
depende de la variable urlpatterns que puede incluir otros URLConfs o el nombre de la vista 
y la ruta para poder acceder a la misma"""
from django.conf.urls import patterns, url

from gestor import views

urlpatterns = patterns('',
    url(r'^hola/$', views.holaView, name='hola'),
    url(r'^registrar/', views.registrarUsuarioView, name='nuevo_usuario'),
    url(r'^save/', views.guardarUsuarioView, name='guardar_nuevo_usuario'),
    url(r'^contactomail/$', views.contactomail, name='contactoMail'),
    url(r'^seteoPassword//(?P<usuario_id>\d+)/$', views.seteoPassword, name='seteoPassword'),
)
