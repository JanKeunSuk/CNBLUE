from django.conf.urls import patterns, include, url
from django.contrib import admin
from gestor import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'supergestor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url(r'^hola/', views.holaView, name='hola'),
    url(r'^registrar/', views.registrarUsuarioView, name='nuevo_usuario'),
    url(r'^save/', views.guardarUsuarioView, name='guardar_nuevo_usuario'),
)
