from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'REPLACE-ME'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: use your actual domain name in production!
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#   }
#}
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'thatlook',
       'USER': 'djangouser',
       'PASSWORD': 'password',
       'HOST': '35.154.111.233',
       'PORT': '3306',
       'OPTIONS': {
           'skip-ssl',
      },
   }
} 


INSTALLED_APPS += [
    'django_extensions',
]

try:
    from .local_settings import *
except ImportError:
    pass
