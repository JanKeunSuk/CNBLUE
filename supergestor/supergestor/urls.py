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
    url(r'^modificarProyecto/(?P<proyecto_id_rec>\d+)/$', views.modificarProyecto, name='modificar_proyecto'),
    url(r'^visualizarProyecto/(?P<proyecto_id_rec>\d+)/$', views.visualizarProyectoView, name='visualizar_proyecto'),
    url(r'^visualizarRol/(?P<rol_id_rec>\d+)/$', views.visualizarRolProyectoView, name='visualizar_rol'),
    url(r'^crearRol/', views.crearRol, name='crear_Rol'),
    url(r'^guardarRol/', views.guardarRolView, name='guardar_nuevo_rol'),
    url(r'^scrum/(?P<proyectoid>\d+)$', views.holaScrumView, name='roles-flujos'),
    url(r'^formarEquipo/$', views.ListarUsuarioParaFormarEquipo, name='formarEquipo'),
    url(r'^crearActividad/$', views.crearActividadView, name='crearActividad'),
    url(r'^modificarActividad/$', views.seleccionarFlujoModificar, name='seleccionarFlujoModificar'),
    url(r'^modificarActividad/(?P<actividad_id_rec>\d+)/$', views.modificarActividad, name='modificarActividad'),
    url(r'^asignarRol/(?P<rolid>\d+)/(?P<proyectoid>\d+)$',views.asignarRol, name= 'asignaRol'),
    
)
