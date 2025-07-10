

from pathlib import Path
import os
import environ


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env()

SECRET_KEY = env('SECRET_KEY')


DEBUG = True

ALLOWED_HOSTS = ["localhost","podhewale.com","127.0.0.1","www.podhewale.com","64.227.131.164"]




INSTALLED_APPS = [  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',    
    'django.contrib.staticfiles',

    'customer',
    'vendor',
    'home',
    'product',
    'common',
    'imagekit',
    'mathfilters',
    'wkhtmltopdf',
    'django_bleach',
    'ckeditor',
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

ROOT_URLCONF = 'podhewale.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'podhewale.wsgi.application'



# Database

if DEBUG:
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': env('ENGINE'),
        'NAME': env('RDSDBNAME'),
        'USER': env("RDSUSERNAME"),
        'PASSWORD': env("RDSPASSWORD"),
        'HOST': env("HOST"),                 
        'PORT': env.int("PORT")
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




LANGUAGE_CODE = 'en-us'

#changed to 'Asia/Calcutta' from UTC

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

#changed to False from True and added datetime format
USE_TZ = False
DATETIME_FORMAT="%Y-%m-%d%H:%M:%S"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CUSTOM FIELDS
# changed user model to common.user

AUTH_USER_MODEL = 'common.User'

# Static and Media Files Settings
STATIC_URL = "/static/"

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]
else:
    STATIC_ROOT =  os.path.join(BASE_DIR, "static/")


MEDIA_URL ="/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Static and Media Files Settings End

EMAIL_HOST = env("EMAIL_HOST")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/customer/login/"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SITE_NAME = env("WEBSITE_NAME")
TAG_LINE = env("TAG_LINE")

RAZORPAYID = env("RAZORID")
RAZORPAYKEY = env("RAZORKEY")

SECRET_ADMIN_URL = env("SECRET_ADMIN_URL")

WEBSITE_NAME = "Podhewale.com"
ADMIN_EMAIL = "admin@podhewale.com"


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline','SelectAll','Strike', 'Subscript', 'Superscript'],
            ['Undo', 'Redo','NumberedList', 'BulletedList','Blockquote', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],            
            ['RemoveFormat', 'Source','Format', 'FontSize'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'Link', 'Unlink', 'Anchor'],
            ['Table', 'HorizontalRule', 'PageBreak']
        ],
        'skin': 'moono',
        'height':150,
        'width': "100%",        
    },
}

#BLEACH SETTINGS
BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a','s','sub','sup','table','tr','td','th']
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style','class','id']
BLEACH_STRIP_TAGS = True
BLEACH_ALLOWED_STYLES = ['font-family','color','background-color', 'font-weight', 'text-decoration', 'font-variant']

# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_SAVE_EVERY_REQUEST = True  # Save session on every request

# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS = 60
# SECURE_HSTS_PRELOAD = True
