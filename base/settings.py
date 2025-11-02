from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party app
    "auth_app.apps.AuthAppConfig",
    # third party package

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

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("PGDB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("POSTDB_NAME", cast=str),
        "USER": config("POSTDB_USER", cast=str),
        "PASSWORD": config("POSTDB_PASSWORD", cast=str),
        "HOST": config("POSTDB_HOST", cast=str),
        "PORT": config("POSTDB_PORT", cast=int),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config("TIME_ZONE", cast=str, default="UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
]

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# config debug toolbar
SHOW_DEBUGGER_TOOLBAR = config("SHOW_DEBUGGER_TOOLBAR", cast=bool, default=True)
if SHOW_DEBUGGER_TOOLBAR:
    INSTALLED_APPS += [
        "debug_toolbar"
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware"
    ]
    INTERNAL_IPS = ["127.0.0.1"]


if config("USE_SSL_CONFIG", cast=bool, default=False):
    # Https/ssl settings
    SECURE_SSL_REDIRECT = True # redirec http request into https request
    USE_X_FORWARDED_HOST = True # use header x-forwarded-host
    USE_X_FORWARDED_PORT = True # use header x-forwarded-port 

    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year, hsts validity period
    SECURE_HSTS_PRELOAD = True # 
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True # active hsts into subdomain

    # coockie
    SESSION_COOKIE_SECURE = True # session cookie only https
    SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN", cast=str) # for example --> .example.com, domain cookie
    SESSION_COOKIE_HTTPONLY = True # prevent access with by javascript

    # csrf
    CSRF_COOKIE_SECURE = True # send cookie csrf only https
    CSRF_COOKIE_HTTPONLY = True # csrf prevent access javascript
    CSRF_COOKIE_SAMESITE = 'Strict' # Prevent cookie requests on cross-site requests
    CSRF_COOKIE_DOMAIN = config("CSRF_COOKIE_DOMAIN", cast=str) # for example --> .example.com, domain csrf cookie
    CSRF_COOKIE_AGE = 3600 # csrf cookie validity period

    # Content Security Settings
    SECURE_CONTENT_TYPE_NOSNIFF = True # prevent mime sniffing
    SECURE_BROWSER_XSS_FILTER = True # active filter xss in browser
    SECURE_REFERRER_POLICY = "strict-origin" # control information  on sourse request
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") 

    # Frame & Clickjacking Protection
    X_FRAME_OPTIONS = "DENY" # prevent show iframe


# cache config
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
if DEBUG:
    CACHES['default']['LOCATION'] = "redis://localhost:6381/1"
else:
    CACHES['default']['LOCATION'] = config("PRODU_REDIS_LOCATION")


# config celery


# config package corsheaders
if DEBUG is False:
    CORS_ALLOWED_ORIGINS = config("PRODUCTION_CORS_ALLOWED_ORIGINS", cast=Csv())
