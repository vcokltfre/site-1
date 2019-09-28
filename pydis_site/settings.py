"""
Django settings for pydis_site project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import secrets
import sys

import environ
from django.contrib.messages import constants as messages

env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = env('DEBUG')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    ALLOWED_HOSTS = env.list(
        'ALLOWED_HOSTS',
        default=[
            'pythondiscord.local',
            'api.pythondiscord.local',
            'admin.pythondiscord.local',
            'staff.pythondiscord.local',
            'web',
            'api.web',
            'admin.web',
            'staff.web'
        ]
    )
    SECRET_KEY = secrets.token_urlsafe(32)

elif 'CI' in os.environ:
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = secrets.token_urlsafe(32)

else:
    ALLOWED_HOSTS = env.list(
        'ALLOWED_HOSTS',
        default=[
            'pythondiscord.com',
            'admin.pythondiscord.com',
            'api.pythondiscord.com',
            'staff.pythondiscord.com',
            'pydis.com',
            'api.pydis.com',
            'admin.pydis.com',
            'staff.pydis.com',
        ]
    )
    SECRET_KEY = env('SECRET_KEY')


# Application definition

INSTALLED_APPS = [
    'pydis_site.apps.api',
    'pydis_site.apps.home',
    'pydis_site.apps.staff',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize.apps.HumanizeConfig',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites.apps.SitesConfig',
    'django.contrib.staticfiles',

    'crispy_forms',
    'django_crispy_bulma',
    'django_hosts',
    'django_filters',
    'django_nyt.apps.DjangoNytConfig',
    'django_simple_bulma',
    'mptt',
    'rest_framework',
    'rest_framework.authtoken',
    'sekizai',
    'sorl.thumbnail',

    'wiki.apps.WikiConfig',

    'wiki.plugins.images.apps.ImagesConfig',
    'wiki.plugins.links.apps.LinksConfig',
    'wiki.plugins.redlinks.apps.RedlinksConfig',
    'wiki.plugins.notifications.apps.NotificationsConfig',  # Required for migrations
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_hosts.middleware.HostsResponseMiddleware',
]
ROOT_URLCONF = 'pydis_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pydis_site', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': [
                'django_hosts.templatetags.hosts_override',
            ],

            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                "sekizai.context_processors.sekizai",
            ],
        },
    },
]

WSGI_APPLICATION = 'pydis_site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'pydis_site', 'static')]
STATIC_ROOT = env('STATIC_ROOT', default='/app/staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = env('MEDIA_ROOT', default='/app/media')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'django_simple_bulma.finders.SimpleBulmaFinder',
]

# django-hosts
# https://django-hosts.readthedocs.io/en/latest/
ROOT_HOSTCONF = 'pydis_site.hosts'
DEFAULT_HOST = 'home'

if DEBUG:
    PARENT_HOST = env('PARENT_HOST', default='pythondiscord.local:8000')

    if ":" in PARENT_HOST:
        ALLOWED_HOSTS.append(PARENT_HOST.split(":", 1)[0])
    else:
        ALLOWED_HOSTS.append(PARENT_HOST)
else:
    PARENT_HOST = env('PARENT_HOST', default='pythondiscord.com')

# Django REST framework
# http://www.django-rest-framework.org
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# Logging
# https://docs.djangoproject.com/en/2.1/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s | %(process)d:%(thread)d | %(module)s | %(levelname)-8s | %(message)s'
            )
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
        'database': {
            'class': 'pydis_site.apps.api.dblogger.DatabaseLogHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'database'],
            'propagate': True,
            'level': env(
                'LOG_LEVEL',
                default=(
                    # If there is no explicit `LOG_LEVEL` set,
                    # use `DEBUG` if we're running in debug mode but not
                    # testing. Use `ERROR` if we're running tests, else
                    # default to using `WARN`.
                    'INFO'
                    if DEBUG and 'test' not in sys.argv
                    else (
                        'ERROR'
                        if 'test' in sys.argv
                        else 'WARN'
                    )
                )
            )
        }
    }
}

# Custom settings for Crispyforms
CRISPY_ALLOWED_TEMPLATE_PACKS = (
    "bootstrap",
    "uni_form",
    "bootstrap3",
    "bootstrap4",
    "bulma",
)

CRISPY_TEMPLATE_PACK = "bulma"

# Custom settings for django-simple-bulma
BULMA_SETTINGS = {
    "variables": {
        "green": "#21c65c",  # Accessibility: Better contrast with the light text
        "primary": "#7289DA",
        "link": "$primary",

        "dimensions": "16 24 32 48 64 96 128 256 512",  # Possible image dimensions
        "navbar-height": "4.75rem",
        "footer-padding": "1rem 1.5rem 1rem",
    }
}

# Required for the wiki
LOGIN_URL = "/admin/login"  # Update this when the real login system is in place
SITE_ID = 1

WIKI_ACCOUNT_HANDLING = False
WIKI_ACCOUNT_SIGNUP_ALLOWED = False

WIKI_ANONYMOUS = True
WIKI_ANONYMOUS_WRITE = False

WIKI_MARKDOWN_KWARGS = {
    "extension_configs": {
        "wiki.plugins.macros.mdx.toc": {
            "anchorlink": True,
            "baselevel": 2
        }
    }, "extensions": [
        "markdown.extensions.abbr",
        "markdown.extensions.attr_list",
        "markdown.extensions.extra",
        "markdown.extensions.footnotes",
        "markdown.extensions.nl2br",
        "markdown.extensions.sane_lists",

        "wiki.core.markdown.mdx.codehilite",
        "wiki.core.markdown.mdx.previewlinks",
        "wiki.core.markdown.mdx.responsivetable",
        "wiki.plugins.macros.mdx.toc",
        "wiki.plugins.macros.mdx.wikilinks",
    ]
}

WIKI_MESSAGE_TAG_CSS_CLASS = {
    messages.DEBUG: "",  # is-info isn't distinctive enough from blurple
    messages.ERROR: "is-danger",
    messages.INFO: "is-primary",
    messages.SUCCESS: "is-success",
    messages.WARNING: "is-warning",
}

WIKI_MARKDOWN_HTML_STYLES = [
    'max-width',
    'min-width',
    'margin',
    'padding',
    'width',
    'height',
]

WIKI_MARKDOWN_HTML_ATTRIBUTES = {
    'img': ['class', 'id', 'src', 'alt', 'width', 'height'],
    'section': ['class', 'id'],
    'article': ['class', 'id'],
}

WIKI_MARKDOWN_HTML_WHITELIST = [
    'article', 'section', 'button'
]
