"""
Django settings for mcdo_coupons project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os
import re
from os import path

import dj_email_url
from decouple import config, Csv


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY', default=None)

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analytical',
    'compressor',
    'bootstrap3',
    'coupons.apps.CouponsConfig',
]

if DEBUG:
    # TODO: Add separate dev config
    INSTALLED_APPS += [
        'django_extensions',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mcdo_coupons.urls'

LOGIN_URL = '/admin/login/'

BASE_URL = config('BASE_URL', default='http://localhost:8000')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mcdo_coupons.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Zurich'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = path.join(BASE_DIR, 'collected-static')

STATIC_URL = '/static/'

NODE_MODULES = path.join(BASE_DIR, 'node_modules')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_OFFLINE = True
COMPRESS_ENABLED = not DEBUG

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'django_compressor_autoprefixer.AutoprefixerFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
)

COMPRESS_AUTOPREFIXER_BINARY = path.join(
    NODE_MODULES, 'postcss-cli/bin/postcss'
)

BOOTSTRAP3 = {
    # Disable emphasizing valid input values
    'success_css_class': '',
}

STATICFILES_DIRS = [
    ('bootstrap', path.join(NODE_MODULES, 'bootstrap/dist/')),
    ('jquery', path.join(NODE_MODULES, 'jquery/dist')),
]


# Email configuration

MANAGERS = config(
    'MANAGERS',
    default='<root@localhost>',
    cast=Csv(
        cast=lambda item: re.search(r'(.*?)\s*<(.+)>', item).groups(),
        delimiter=','
    ),
)

SERVER_EMAIL = config('SERVER_EMAIL', 'McDo Bons <root@localhost>')
EMAIL_SUBJECT_PREFIX = ''

email_config = config('EMAIL_URL', default='console://', cast=dj_email_url.parse)
EMAIL_FILE_PATH = email_config['EMAIL_FILE_PATH']
EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']
EMAIL_HOST = email_config['EMAIL_HOST']
EMAIL_PORT = email_config['EMAIL_PORT']
EMAIL_BACKEND = email_config['EMAIL_BACKEND']
EMAIL_USE_TLS = email_config['EMAIL_USE_TLS']
EMAIL_USE_SSL = email_config['EMAIL_USE_SSL']


PIWIK_DOMAIN_PATH = config('PIWIK_DOMAIN_PATH', default=None)
PIWIK_SITE_ID = config('PIWIK_SITE_ID', default=None)
