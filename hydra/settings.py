"""
Django settings for hydra project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import base64
import json
import os
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", 'django-insecure-ql-07ycqh79^iqi@@#6w9am@-*q*pu9%-3krxq8f8y+j4e%w+z')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'easy_thumbnails',
    'image_cropping',
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

ROOT_URLCONF = 'hydra.urls'

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

WSGI_APPLICATION = 'hydra.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dist'),
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Base url to serve media files
MEDIA_URL = '/media/'
# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
UPLOADED_IMAGES_PATH = os.path.join(os.path.join(BASE_DIR, 'media'), 'uploaded_images')


# django-image-cropping

from easy_thumbnails.conf import Settings as thumbnail_settings

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS


# Board/shape settings
HEAD_SEQUENCES = [
    ('n', 'e', 's', 'w'),
    ('e', 's', 'w', 'n'),
    ('s', 'w', 'n', 'e'),
    ('w', 'n', 'e', 's'),
]
LIMB_SEQUENCES = [
    ('nw', 'ne', 'se', 'sw'),
    ('ne', 'se', 'sw', 'nw'),
    ('se', 'sw', 'nw', 'ne'),
    ('sw', 'nw', 'ne', 'se'),
]
PIECE_SHAPES = [
    dict(key='1', heads='n', name='1 Head'),
    dict(key='2', heads='wn', name='2 Heads'),
    dict(key='3', heads='wne', name='3 Heads'),
    dict(key='4', heads='nesw', name='4 Heads'),
    dict(key='c', heads='ns', name='Classic'),
    dict(key='x', heads='', name='X'),
]
OPPOSING_SIDES = [2, 3, 0, 1]
# Format is <key>+<turns> where each turn is 90 degrees clockwise, and the default orientation is the shape image
DEFAULT_GRID = """
W1siNCswIiwiMisxIiwiYyswIiwiMiswIiwiMyswIiwiYyswIiwiMyswIiwiMisxIiwiMisxIiwiMSswIiwiMiswIiwiNCswIiwiYyswIiwiMyswI
iwiMisxIiwiYyswIiwiNCswIiwiMSswIiwiMyszIiwiMyswIiwiYyswIiwiMyswIiwiMysxIl0sWyIyKzMiLCIzKzAiLCIyKzIiLCIyKzEiLCIzKz
EiLCJ4KzEiLCIzKzMiLCIzKzAiLCIyKzEiLCIzKzEiLCIzKzEiLCIxKzIiLCJjKzEiLCIyKzEiLCJjKzAiLCIzKzIiLCJ4KzAiLCIzKzAiLCIxKzI
iLCIyKzAiLCIyKzMiLCI0KzAiLCIyKzIiXSxbIjIrMiIsIjErMCIsIjMrMiIsIjMrMSIsIjErMSIsIjMrMSIsIjErMSIsIjMrMSIsIjIrMSIsIngr
MCIsIjErMyIsIjErMyIsIjIrMCIsIjMrMCIsIjErMiIsIjErMyIsIjIrMCIsIjMrMCIsIjErMSIsIjErMCIsImMrMSIsIjErMiIsIjMrMiJdLFsiY
ysxIiwiMysxIiwieCswIiwiYysxIiwiYyswIiwiMiszIiwiMyszIiwiYysxIiwiYyswIiwiMyswIiwiYyswIiwiMyszIiwiMyszIiwiMyswIiwiMS
sxIiwiMisxIiwiMysxIiwiMysxIiwiYyswIiwiMyszIiwiMyswIiwieCswIiwiMysyIl0sWyIzKzMiLCIzKzIiLCIyKzEiLCJjKzAiLCJjKzEiLCJ
4KzEiLCIxKzMiLCIzKzAiLCIxKzEiLCIyKzEiLCJ4KzAiLCIyKzMiLCJjKzEiLCIyKzEiLCJjKzAiLCIyKzAiLCIyKzMiLCIzKzIiLCIxKzEiLCIy
KzIiLCIzKzEiLCIzKzEiLCIyKzIiXSxbIjIrMyIsIjIrMyIsIjMrMyIsImMrMSIsIjErMCIsIjMrMCIsIjMrMSIsIjIrMSIsImMrMCIsIjQrMCIsI
mMrMCIsIjErMyIsIjIrMCIsIjMrMyIsIjMrMiIsImMrMCIsIjErMyIsImMrMSIsIjIrMSIsIjErMSIsIngrMCIsIjErMyIsIjMrMiJdLFsiMiszIi
wiYysxIiwieCswIiwiNCswIiwiYyswIiwiMyswIiwieCswIiwiMiswIiwiMiszIiwiMiszIiwiYysxIiwiMSswIiwiNCswIiwieCswIiwiMSszIiw
iYysxIiwiYyswIiwiMiswIiwiMyszIiwiMyszIiwiNCswIiwiYyswIiwiMysyIl0sWyJjKzEiLCIzKzEiLCJjKzAiLCIxKzMiLCJjKzEiLCIyKzEi
LCIxKzAiLCI0KzIiLCIxKzEiLCIxKzIiLCIzKzAiLCJjKzIiLCJjKzEiLCIzKzEiLCIzKzEiLCJjKzAiLCIxKzMiLCIyKzAiLCIxKzMiLCJjKzEiL
CJ4KzAiLCIyKzMiLCJjKzEiXSxbIjQrMCIsIjErMSIsIjErMiIsIjIrMCIsIjIrMCIsIjQrMiIsImMrMCIsIjIrMyIsIjMrMCIsIjIrMiIsIjIrMS
IsIjIrMiIsIjErMCIsIjMrMiIsIjErMSIsIjIrMiIsIjErMCIsIjMrMyIsIjIrMCIsIjQrMCIsImMrMCIsImMrMSIsIjIrMSJdLFsiMiszIiwiMis
wIiwiYyszIiwiMSswIiwiNCsyIiwiMSsyIiwiYyszIiwiMisyIiwiYysyIiwiMSszIiwiMyszIiwiMSszIiwiMyswIiwiMSsxIiwiMisxIiwiMisy
IiwiMSswIiwiYysxIiwiMSswIiwiMSszIiwiMysyIiwiMysxIiwiMysxIl0sWyIzKzIiLCIyKzEiLCIxKzAiLCIyKzAiLCIyKzMiLCIzKzIiLCIxK
zAiLCJjKzEiLCIyKzIiLCIzKzEiLCIxKzIiLCIyKzAiLCIzKzAiLCIyKzEiLCJjKzIiLCIyKzMiLCIzKzMiLCIzKzAiLCIyKzEiLCIxKzAiLCIyKz
MiLCJjKzEiLCIxKzEiXSxbIjErMyIsIjMrMCIsIjErMCIsIjQrMyIsIjErMSIsIjErMiIsIjQrMCIsIjErMCIsIjErMyIsIjErMyIsImMrMyIsIjI
rMSIsIjIrMSIsIjErMCIsIjErMyIsIjErMyIsImMrMSIsIjMrMSIsIjMrMSIsIjMrMSIsIngrMCIsIjIrMCIsIjMrMCJdLFsiMyswIiwiMysxIiwi
MisxIiwiMisyIiwiMisxIiwiMSsyIiwiYyszIiwiYyswIiwiMiswIiwiNCswIiwiMSswIiwiMiswIiwiMiswIiwiNCswIiwiMysxIiwiMisxIiwiY
yswIiwiYysxIiwiMSsxIiwieCswIiwiMyszIiwiMyszIiwiNCswIl0sWyI0KzAiLCJ4KzIiLCI0KzMiLCJ4KzEiLCIzKzMiLCIyKzMiLCIzKzAiLC
IxKzIiLCIyKzAiLCIzKzIiLCIzKzEiLCIzKzEiLCIyKzEiLCIxKzIiLCIyKzMiLCIyKzAiLCIxKzMiLCIyKzAiLCIyKzAiLCI0KzAiLCIxKzEiLCI
xKzEiLCIyKzIiXSxbIjErMyIsIjIrMCIsIjIrMyIsIjMrMCIsIjErMiIsImMrMyIsIjErMCIsIjMrMiIsImMrMCIsIjErMyIsIjMrMiIsIjErMSIs
IjIrMSIsIjErMiIsImMrMSIsImMrMCIsIjMrMyIsIjMrMyIsIjIrMCIsIjIrMyIsIjMrMyIsIjIrMCIsIjMrMiJdLFsiMyszIiwiMyszIiwiMiszI
iwiMyszIiwiMysyIiwiMisxIiwiMysxIiwiMSsyIiwiMiszIiwiMyswIiwiMSsyIiwiNCswIiwiMSswIiwiMiszIiwiMiswIiwiMysyIiwiMisyIi
wiMisyIiwiMysxIiwiMisyIiwiMSsxIiwiMSswIiwiMysyIl0sWyIyKzMiLCIzKzIiLCIxKzIiLCIyKzMiLCIyKzMiLCIyKzAiLCJjKzEiLCIyKzI
iLCIyKzIiLCJjKzAiLCIyKzMiLCJjKzEiLCIyKzEiLCJ4KzAiLCI0KzMiLCIxKzEiLCIyKzIiLCIyKzIiLCJ4KzMiLCIyKzMiLCIzKzAiLCIxKzAi
LCIzKzIiXSxbImMrMSIsIjIrMiIsIjErMSIsIjIrMiIsIjErMiIsIjMrMyIsIjMrMyIsImMrMyIsIjErMiIsImMrMSIsIjErMiIsIjQrMSIsImMrM
CIsIjMrMCIsIjErMSIsImMrMiIsIjErMyIsIjIrMyIsIjQrMCIsIngrMCIsIjIrMCIsIjIrMCIsImMrMSJdLFsiNCswIiwiMSsxIiwiMysxIiwiMS
syIiwiMysyIiwieCswIiwiMysyIiwiMysxIiwieCsxIiwiMyszIiwiMSszIiwiMysyIiwieCsyIiwiNCszIiwiMysxIiwieCsxIiwiNCsxIiwiMSs
xIiwieCswIiwiMyszIiwiMyszIiwiMiswIiwiMyswIl0sWyJjKzEiLCIxKzAiLCJjKzEiLCIyKzIiLCJ4KzAiLCIzKzAiLCIxKzIiLCIzKzIiLCJj
KzAiLCIzKzIiLCIyKzEiLCIyKzIiLCIzKzEiLCIxKzIiLCIyKzMiLCI0KzMiLCIxKzEiLCIzKzEiLCIzKzEiLCIxKzIiLCIyKzMiLCIyKzAiLCI0K
zAiXSxbIjQrMCIsIjMrMSIsImMrMCIsImMrMSIsIjErMCIsIjIrMCIsIjMrMiIsIjErMiIsIjMrMiIsIjErMiIsIjMrMyIsIjMrMiIsIjErMSIsIj
IrMiIsIjErMiIsIjErMyIsIjMrMyIsImMrMSIsIjErMiIsIjErMyIsIjErMyIsIjMrMCIsIjIrMiJdLFsiMiszIiwiMiszIiwiMiszIiwiNCswIiw
iYyswIiwiNCswIiwiMisyIiwiMSsyIiwiMiszIiwiMiszIiwiMysyIiwiMSsyIiwiMyszIiwiMiszIiwiMiszIiwiMyszIiwiMiszIiwiNCswIiwi
MisyIiwiMysxIiwiYyswIiwiMyszIiwiMysyIl1d
"""
GRID = json.loads(base64.b64decode(env('GRID', DEFAULT_GRID)).decode('utf-8'))
GRID_ROWS = len(GRID)
GRID_COLS = len(GRID[0])
for r in GRID:
    assert len(r) == GRID_COLS, "Each row must have the same number of cols"
# If True, only the shapes will be rendered in the grid, not the placed pieces
GRID_ONLY = env.bool('GRID_ONLY', False)
SCROLL_TOP_DELAY = env.int('SCROLL_TOP_DELAY', 300)
PIECE_QUERY_LIMIT = env.int('PIECE_QUERY_LIMIT', 30)
