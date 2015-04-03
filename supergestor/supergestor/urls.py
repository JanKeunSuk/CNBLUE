# coding: utf-8
"""
URLconf es un archivo incluye función vista asociada, que se pasan directamente como un método.
Importamos las funciones view y agregamos las vistas de holaView, registrarUsuarioView y guardarUsuarioView 
Tambien incluimos otros modulos URLconf como include(admin.site.urls) y include('django.contrib.auth.urls').
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from gestor import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url(r'^hola/', views.holaView, name='hola'),
    url(r'^registrar/', views.registrarUsuarioView, name='nuevo_usuario'),
    url(r'^save/', views.guardarUsuarioView, name='guardar_nuevo_usuario'),
    url(r'^contactomail/$', views.contactomail, name='contactoMail'),
    url(r'^seteoPassword/(?P<usuario_id>\d+)/$', views.seteoPassword, name='seteoPassword'),
    url(r'^scrum/$', views.holaScrumView, name='roles-flujos'),
    url(r'^formarEquipo/$', views.ListarUsuarioParaFormarEquipo, name='formarEquipo'),
)
