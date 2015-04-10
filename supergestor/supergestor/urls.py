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
    url(r'^modificarProyecto/(?P<usuario_id>\d+)/(?P<proyecto_id_rec>\d+)/$', views.modificarProyecto, name='modificar_proyecto'),
    url(r'^visualizarProyecto/(?P<usuario_id>\d+)/(?P<proyecto_id_rec>\d+)/$', views.visualizarProyectoView, name='visualizar_proyecto'),
    url(r'^visualizarRol/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/(?P<rol_id_rec>\d+)/$', views.visualizarRolProyectoView, name='visualizar_rol'),
    url(r'^crearRol/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/', views.crearRol, name='crear_Rol'),
    url(r'^guardarRol/(?P<usuario_id>\d+)/', views.guardarRolView, name='guardar_nuevo_rol'),
    url(r'^visualizarFlujo/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/(?P<flujo_id_rec>\d+)/$', views.visualizarFlujoProyectoView, name='visualizar_flujo'),
    url(r'^modificarFlujo/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/(?P<flujo_id_rec>\d+)/$', views.modificarFlujo, name='modificar_flujo'),
    url(r'^modificarRol/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/(?P<rol_id_rec>\d+)/$', views.modificarRol, name='modificar_rol'),
    url(r'^crearFlujo/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/', views.crearFlujo, name='crear_Flujo'),
    url(r'^guardarFlujo/', views.guardarFlujoView, name='guardar_nuevo_flujo'),
    url(r'^scrum/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/$', views.holaScrumView, name='roles-flujos'),
    url(r'^crearActividad/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/$', views.crearActividadView, name='crearActividad'),
    url(r'^modificarActividad/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/$', views.seleccionarFlujoModificar, name='seleccionarFlujoModificar'),
    url(r'^modificarActividad/(?P<usuario_id>\d+)/(?P<proyectoid>\d+)/(?P<actividad_id_rec>\d+)/$', views.modificarActividad, name='modificarActividad'),
    url(r'^asignarRol/(?P<usuario_id>\d+)/(?P<rolid>\d+)/(?P<proyectoid>\d+)$',views.asignarRol, name= 'asignaRol'),
    url(r'^equipoProyecto/(?P<proyecto_id_rec>\d+)/(?P<usuario_id>\d+)$',views.listarEquipo,name='listaEquipo'),
    
)
