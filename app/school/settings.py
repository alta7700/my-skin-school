from pathlib import Path

SETTINGS_DIR = Path(__file__).resolve().parent
BASE_DIR = SETTINGS_DIR.parent

if (SETTINGS_DIR / '.env').exists():
    from dotenv import dotenv_values
    env = dotenv_values(SETTINGS_DIR / '.env')
    DEBUG_DEFAULT = 'true'
else:
    from os import environ
    env = {**environ}
    DEBUG_DEFAULT = 'false'

SECRET_KEY = env['SECRET_KEY']
DEBUG = env.get('DEBUG', DEBUG_DEFAULT).lower() == 'true'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main.apps.MainConfig',
    'users.apps.UsersConfig',
    'tickets.apps.TicketsConfig',
    'lessons.apps.LessonsConfig',
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

ROOT_URLCONF = 'school.urls'

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

WSGI_APPLICATION = 'school.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env['DB_NAME'],
        'USER': env['DB_USER'],
        'PASSWORD': env['DB_PASSWORD'],
        'HOST': env['DB_HOST'],
        'PORT': env['DB_PORT'],
    }
}


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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


def list_from_env(name: str, required=False, sep=','):
    value = env.get(name, '')
    assert value if required else True, f'{name} must be in env'
    return [item for item in value.split(sep) if item]


ALLOWED_HOSTS = list_from_env('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = list_from_env('CSRF_TRUSTED_ORIGINS')

AUTHENTICATION_BACKENDS = ['users.backends.AuthBackend']
AUTH_USER_MODEL = 'users.User'

PHONENUMBER_DEFAULT_REGION = 'RU'
PHONENUMBER_DEFAULT_FORMAT = 'E164'
