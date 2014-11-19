# Django settings for enhydris project.
# coding=UTF-8
from django.utils.translation import ugettext_lazy as _
import os

TEMPLATE_DEBUG = True
DEBUG = True
PROJECT_DIR = os.path.dirname(__file__)

ROOT_URLCONF = 'unexe.urls'

LANGUAGES = (
        ('en', _('English')),
        ('el', _('Greek')),
        ('pt', _('Portuguese')),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, "locale/"),
)

LANGUAGE = 'en'

ADMINS = (
    ('Stefanos Kozanis', 'S.Kozanis@itia.ntua.gr'),
)

ALLOWED_HOSTS = ['127.0.0.1', '83.212.168.149']

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'iwidget',
        'USER': 'iwidget',
        'PASSWORD': 'iwidget_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

TIME_ZONE = 'Europe/Athens'

SITE_ID = 1
SITE_URL = "83.212.168.149/iwidget/"

MEDIA_ROOT = os.path.join(PROJECT_DIR, "media/")
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_DIR, "staticfiles/")
STATIC_URL = '/static/'

POSTGIS_VERSION = (2, 1, 2)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'asd$Gfkl6%$2bkfla$gjg0sjgk4lw9g$Gr4itlrki4T4g%hfdb'

# GentityFile upload directory (must be relative path and it'll be created
# under site_media dir)
GENTITYFILE_DIR = 'gentityfile'

#Uncoment to hide open layers map
#USE_OPEN_LAYERS = False
#Uncoment to alter the default value of min viewport
#MIN_VIEWPORT_IN_DEGS = 0.04
#Map default area (minlong, minlat, maxlong, maxlat)
MAP_DEFAULT_VIEWPORT = (19.3, 34.75, 29.65, 41.8)

# Options for django-registration
ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.my.domain'
DEFAULT_FROM_EMAIL = 'user@host.domain'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST_USER = 'automaticsender@my.domain'
EMAIL_HOST_PASSWORD = 'mypassword'

#Set login redirection as apropriate in the cases
#of site installed on a subdirectory
#for http://my.site/my_dir/ set it to /my_dir/
#LOGIN_REDIRECT_URL='/my_dir/'
#If you uncomment the above line, please uncomment
#the line bellow as well to update LOGIN_URL correctly
#LOGIN_URL=LOGIN_REDIRECT_URL+'accounts/login'

#Change SESSION_COOKIE_NAME if more than one django
#sites on a single domain, or other sites with
# sessionid is already set (defaul: sessionid)
#SESSION_COOKIE_NAME='sessionid'

#Set custom cookies expiration (default is 2 weeks
#that is 1209600 seconds).
#SESSION_COOKIE_AGE=2419200

# Options for political divisions
FILTER_DEFAULT_COUNTRY = 'GREECE'
FILTER_POLITICAL_SUBDIVISION1_NAME = _('District')
FILTER_POLITICAL_SUBDIVISION2_NAME = _('Prefecture')

USERS_CAN_ADD_CONTENT = False
SITE_CONTENT_IS_FREE = False
TSDATA_AVAILABLE_FOR_ANONYMOUS_USERS = False
STORE_TSDATA_LOCALLY = True

#Display copyright information on web pages (station detail and time
#series detail)
DISPLAY_COPYRIGHT_INFO = False

#This is a way to filter all station data site_wide with some
#criteria.
#SITE_STATION_FILTER = {'owner__id__exact': '9',}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    #'django.contrib.markup',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.gis',

    'rest_framework',
    'south',
    'registration',
    'profiles',
    'ajax_select',
    'sekizai',
    'captcha',
    'django_tables2',

    'enhydris.dbsync',
    'enhydris.hcore',
    'enhydris.hprocessor',
    'enhydris.hchartpages',
    'enhydris.sorting',
    'enhydris.api',
    'enhydris.permissions',
    'tl',
    'uc_03_1',
    'uc_03_6',
    'uc_01_2',
    'uc_02_1',
    'iwidget',
    'unexe',
    'csv_parser',
    'core',
    'sso',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django_notify.middleware.NotificationsMiddleware',
    'enhydris.sorting.middleware.SortingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

APPEND_SLASH = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django_notify.context_processors.notifications',
    "django.core.context_processors.csrf",
    'sekizai.context_processors.sekizai',
    'unexe.context_processors.initialise',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates/"),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)


AUTH_PROFILE_MODULE = 'hcore.UserProfile'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = LOGIN_REDIRECT_URL+'accounts/login'

#ENHYDRIS_TS_GRAPH_CACHE_DIR = '/tmp/iwidget_restapi_series_cache'
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#        'LOCATION': '/var/tmp/iwidget_restapi_cache',
#    }
#}

EMAIL_HOST = 'mail.sch.gr'
EMAIL_HOST_USER = 'xpanta'
EMAIL_HOST_PASSWORD = 'tre5183'
DEFAULT_FROM_EMAIL = 'no-reply@iwidget.up-ltd.co.uk'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'ERROR',
        },
        'iwidget': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'enhydris': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'csv_parser': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'uc_03_1': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
