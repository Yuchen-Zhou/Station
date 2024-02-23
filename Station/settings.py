import os.path
import os
from pathlib import Path
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k3k1tb@ff^5!=dw2*%nlds4)dfe%c5k)w+iw1yfeeya5kif!gv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '47.97.204.127', '127.0.0.1'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'back',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', #安全机制，保护用户与网站的通信安全
    'django.contrib.sessions.middleware.SessionMiddleware', #会话Session功能
    # 添加中间件 LocalMiddleware
    'django.middleware.locale.LocaleMiddleware', #国际化和本地化功能
    'django.middleware.common.CommonMiddleware', #处理请求信息，规范化请求内容
    'django.middleware.csrf.CsrfViewMiddleware', #开启CSRF防护功能
    'django.contrib.auth.middleware.AuthenticationMiddleware', #内置的用户认证系统
    'django.contrib.messages.middleware.MessageMiddleware', #内置的信息提示功能
    'django.middleware.clickjacking.XFrameOptionsMiddleware', #防止恶意程序单机劫持
]

AUTH_USER_MODEL = 'back.CustomUser'
ROOT_URLCONF = 'Station.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'Station.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'station',
        'USER': 'root',
        'PASSWORD': 'zyc010804',
        'HOST': '47.97.204.127',
        'PORT': '3306'
    },

}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# 设置根目录的静态资源文件夹
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
        os.path.join(BASE_DIR, 'back/static')
    ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# 设置媒体路由地址信息
MEDIA_URL = '/media/'
# 获取media文件夹的完整路径信息
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'login'



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGS_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'user_activity.log'),
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'loggers': {
        'user_activity': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


