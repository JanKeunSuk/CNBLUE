# coding: utf-8
"""
Django settings es un supergestor de proyecto, que contiene toda la configuración necesaria.
Agregamos en INSTALLED_APPS 'gestor'.
Se especificaron las rutas de ROOT_URLCONF,WSGI_APPLICATION,AUTH_USER_MODEL (usuario para el modulo de autenticación) y los templates.
La configuración de la Base de Datos utilizando Postgresql
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cu*_(rwgi$db-20p(*+fy7%3t!$uxhjoc$ccw8%rw@o7k-2%22'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition



INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestor',
)
"""Definición de aplicaciones. Se agrego en la INSTALLED_APPS gestor."""

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



ROOT_URLCONF = 'supergestor.urls'
"""Ubicación de la urls.py dentro de supergestor"""

WSGI_APPLICATION = 'supergestor.wsgi.application'
"""Ubicación del wsgi.py dentro de supergestor"""

AUTH_USER_MODEL='gestor.MyUser'
"""Ubicación del modelo usuario para el modulo de autenticación"""


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
"""Ubicación del templates"""
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
"""Configuración de la Base de Datos utilizando Postgresql"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'prueba5', #la base prueba 3 es para el primer intento de migrar modelos de IS"
        'USER': 'seba2',# seba2 es owner de prueba3
        'PASSWORD': 'seba2',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# EMAIL SETTINGS
EMAIL_HOST = 'smtp.gmail.com'
 
EMAIL_HOST_USER = 'usuariodjango@gmail.com'
 
EMAIL_HOST_PASSWORD = 'usuariodjango2015'
 
EMAIL_PORT = 587
 
EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


