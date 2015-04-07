
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
    url(r'^modificarProyecto/(?P<proyecto_id_rec>\d+)/$', views.modificarProyecto, name='modificar_proyecto'),
    url(r'^visualizarProyecto/(?P<proyecto_id_rec>\d+)/$', views.visualizarProyectoView, name='visualizar_proyecto'),
    url(r'^visualizarRol/(?P<rol_id_rec>\d+)/$', views.visualizarRolProyectoView, name='visualizar_rol'),
    url(r'^crearRol/', views.crearRol, name='crear_Rol'),
    url(r'^guardarRol/', views.guardarRolView, name='guardar_nuevo_rol'),
    url(r'^scrum/$', views.holaScrumView, name='roles-flujos'),
    url(r'^formarEquipo/$', views.ListarUsuarioParaFormarEquipo, name='formarEquipo'),
    url(r'^crearActividad/$', views.crearActividadView, name='crearActividad'),
    url(r'^modificarActividad/$', views.seleccionarFlujoModificar, name='seleccionarFlujoModificar'),
    url(r'^modificarActividad/(?P<actividad_id_rec>\d+)/$', views.modificarActividad, name='modificarActividad'),
)
