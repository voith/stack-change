"""
Django settings for stack_change project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE_PATH = os.path.join(BASE_DIR, '.env')
if os.path.exists(ENV_FILE_PATH):
    print('loading from .env')
    load_dotenv(ENV_FILE_PATH)
else:
    print('.env not found. Loading from /etc/environment')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e1)%abshsd9^7lln(lnmjby+6=7=gim$vbmi6&)r4(r@t^$6h@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'social_django',
    'rest_framework',
    'django_filters',
    'rest_framework_social_oauth2',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'stackXchange.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'stackXchange/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'stackXchange.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'app.User'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'stackXchange/templates/static')
]

STACK_EXCHANGE = {
    'SECRET': os.getenv('STACK_EXCHANGE_SECRET'),
    'KEY': os.getenv('STACK_EXCHANGE_KEY'),
    'CLIENT_ID': os.getenv('STACK_EXCHANGE_CLIENT_ID'),
    'OAUTH_DOMAIN': os.getenv('STACK_EXCHANGE_OAUTH_DOMAIN'),
    'APP_WEBSITE': os.getenv('STACK_EXCHANGE_APP_WEBSITE'),
    'REDIRECT_URI': os.getenv('STACK_EXCHANGE_APP_WEBSITE'),
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
}

AUTHENTICATION_BACKENDS = (
   'django.contrib.auth.backends.ModelBackend',
   'stackXchange.oauth_backend.StackoverflowOAuth2V2',
)

LOGIN_URL = 'so_login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_STACKOVERFLOW_KEY = STACK_EXCHANGE['CLIENT_ID']
SOCIAL_AUTH_STACKOVERFLOW_API_KEY = STACK_EXCHANGE['KEY']
SOCIAL_AUTH_STACKOVERFLOW_SECRET = STACK_EXCHANGE['SECRET']
SOCIAL_AUTH_STACKOVERFLOW_SCOPE = ['read_inbox', 'no_expiry']
SOCIAL_AUTH_STACKOVERFLOW_USER_FIELDS = ['username', 'email', 'access_token', 'account_id']
SOCIAL_AUTH_USER_FIELDS = ['username', 'email', 'access_token', 'account_id']
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'app.pipeline.save_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

IPC_PATH = os.environ['IPC_PATH']
CONTRACT_ADDRESS = os.environ['CONTRACT_ADDRESS']