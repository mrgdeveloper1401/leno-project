import os
from pathlib import Path
from decouple import config, Csv
from django.utils import timezone
from kombu import Queue

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', cast=str, default='Hello World!')

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
    "django_celery_results",
    "django_celery_beat"

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

# WSGI_APPLICATION = 'base.wsgi.application'
ASGI_APPLICATION = "base.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("PGDB_ENGINE", default="django.db.backends.postgresql", cast=str),
        "NAME": config("POSTDB_NAME", cast=str, default="postgres"),
        "USER": config("POSTDB_USER", cast=str, default="postgres"),
        "PASSWORD": config("POSTDB_PASSWORD", cast=str, default="postgres"),
        "HOST": config("POSTDB_HOST", cast=str, default="127.0.0.1"),
        "PORT": config("POSTDB_PORT", cast=int, default=5432),
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
    CACHES['default']['LOCATION'] = config("PRODU_REDIS_LOCATION", cast=str)


# config package corsheaders
if DEBUG is False:
    CORS_ALLOWED_ORIGINS = config("PRODUCTION_CORS_ALLOWED_ORIGINS", cast=Csv())

# config session cache
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# login conf
# if user not authenticate redirect into route login
LOGIN_URL = "/auth/request_phone/"

# celery config
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300
CELERY_CACHE_BACKEND = 'default'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_WORKER_CONCURRENCY = os.cpu_count()
if DEBUG:
    CELERY_BROKER_URL = "redis://localhost:6381/2"
    # CELERY_RESULT_BACKEND = "redis://localhost:6381/3"
else:
    CELERY_BROKER_URL = config("CELERY_BROKER_URL", cast=str)
    # CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", cast=str)

# config celery beat
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# celery queue
CELERY_TASK_QUEUES = {
    Queue("refresh_token"),
    Queue("logout_user")
}

if config("USER_WHITENOISE", cast=bool, default=True):
    MIDDLEWARE += [
        "whitenoise.middleware.WhiteNoiseMiddleware"
    ]

# config storages
STORAGES = {
    'default':
        {
            'BACKEND': config("STORAGE_BACKEND", cast=str, default='django.core.files.storage.FileSystemStorage'),
        },
    'staticfiles':
        {
            'BACKEND': config("STORAGE_STATIC_FILES", cast=str, default='whitenoise.storage.CompressedManifestStaticFilesStorage'),
        }
}

if config("USER_LOG", cast=bool, default=True):
    log_dir = os.path.join('general_log_django', timezone.now().strftime("%Y-%m-%d"))
    os.makedirs(log_dir, exist_ok=True)
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "color": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(levelname)s %(reset)s%(asctime)s %(module)s %(process)d %(thread)d %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "error_file": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "formatter": "color",
                "filename": os.path.join(log_dir, 'error_file.log')
            },
            "warning_file": {
                "level": "WARN",
                "class": "logging.FileHandler",
                "formatter": "color",
                "filename": os.path.join(log_dir, 'warning_file.log')
            },
            "critical_file": {
                "level": "CRITICAL",
                "class": "logging.FileHandler",
                "formatter": "color",
                "filename": os.path.join(log_dir, 'critical_file.log')
            },
        },
        "loggers": {
            "django": {
                "handlers": ["warning_file", "critical_file", "error_file"],
                'propagate': True,
            }
        }
    }
