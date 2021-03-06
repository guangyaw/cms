"""
Django settings for cms project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(a+916@*vd2n(a04l3mu)(09bln$qex&^zq@0dsri5(=^kv)br'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['cms.twshop.asia', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'accounts',
    'blogs',
    'django_q',
    'coins'
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

ROOT_URLCONF = 'cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'guangyaw_django',                       # Or path to database file if using sqlite3.
#         'USER': 'guangyaw_dxyaw',                       # Not used with sqlite3.
#         'PASSWORD': 'password',               # Not used with sqlite3.
#         'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'common_static'),
)


# ckeditor
#CKEDITOR_JQUERY_URL ='https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js'
# 放在django 專案根目录，同时也需要新建media資料夾
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'
CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Full': [
            [ 'Source','-','Save','NewPage','DocProps','Preview','-','Templates' ],
            [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ],

            [ 'Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ],
            [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField' ],
            '/',
            [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ],
            [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv', '-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ],
            [ 'Link','Unlink','Anchor' ],
            [ 'Image','Table','HorizontalRule','Smiley','SpecialChar','PageBreak','Iframe' ],
            '/',
            [ 'Styles','Format','Font','FontSize' ] ,
            [ 'TextColor','BGColor' ] ,
            [ 'Maximize', 'ShowBlocks','-','About' ] ,
            ['CodeSnippet'],  #代码段按钮

        ],
        'toolbar': 'Full',
        'extraPlugins': 'codesnippet',   #代码段插件
    }
}

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 1,
    'timeout': 1800,
    'retry': 20,
    'queue_limit': 2,
    'bulk': 10,
    'orm': 'default'
}