##this file contains the settings for the django project. It is used to configure the project and its apps. 
#It is also used to configure the database, static files, and other settings.
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent #sets the base directory and creates paths to other files in the project

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ada3%9i36+b14aivsp8h1of5qpohg24jw=_wsw^popnho@o1rq' ##secret key fo rth eproject used to sign cookies and other security-related things.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #itshould be false for the production env

ALLOWED_HOSTS = [] 


# Application definition
#list of apps that are installed in the project. These apps can be used to add functionality to the project.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'notices',
]
#middleware is used to process requests and responses in the project. It can be used to add functionality to the project, such as authentication, security, and caching.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#It is used to route requests to the appropriate views.
ROOT_URLCONF = 'config.urls'

# It is used to configure the template engine and the template directories.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
#WSGI is a specification for a universal interface between the web server and web applications for the Python programming language.
WSGI_APPLICATION = 'config.wsgi.application'

#It is used to configure the database engine, name, user, password, host, and port.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# User-uploaded files (e.g. posters/images attached to posts in later stages)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'notice_list'
LOGOUT_REDIRECT_URL = 'login'
