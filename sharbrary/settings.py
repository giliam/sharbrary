# coding:utf-8
"""
Django settings for sharbrary project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import parameters

from django.template.base import add_to_builtins

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

USE_X_FORWARDED_HOST = False
FORCE_SCRIPT_NAME = ""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'IsOverridenBySomeLocalSettingsValue'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_wysiwyg',
    'tinymce',
    'django.contrib.humanize',
    'library',
    'sharing'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'sharbrary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': parameters.TEMPLATES_DIRS if parameters.TEMPLATES_DIRS else ["C:/Users/Dev/Documents/divers/wamp/www/15reservation/GitPortable/Data/home/biblib/sharbrary/templates"],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'sharbrary.wsgi.application'

# Auth configuration

LOGIN_URL = 'login'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'SomeDatabaseName', 
    'USER': 'SomeUserName', 
    'PASSWORD': 'SomePassword',
    'HOST': 'localhost',
    'PORT': '',
  }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda x: x

LANGUAGES = (
   ('fr', gettext('Français')),
   ('en', gettext('English')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, '/locale/'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = FORCE_SCRIPT_NAME + "/static/"
STATIC_ROOT = BASE_DIR + '/static/'

STATICFILES_DIRS = parameters.STATICFILES_DIRS if parameters.STATICFILES_DIRS else (
    "assets/",
)

MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = FORCE_SCRIPT_NAME + "/media/"

# Adds auto loading of staticfiles and i18n tags.
add_to_builtins('django.templatetags.i18n')
add_to_builtins('django.contrib.humanize.templatetags.humanize')
add_to_builtins('django.contrib.staticfiles.templatetags.staticfiles')

#Loads local settings that rewrite the settings SECRET_KEY and DATABASES.
from settings_local import *
