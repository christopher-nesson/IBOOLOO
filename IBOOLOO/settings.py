"""
Django settings for IBOOLOO project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0_=jwkzt3y3fh62slu^02%h)e88zx)7w3aol9oq80g#e9vbzx@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'UserApp.apps.UserappConfig',
    'MainApp.apps.MainappConfig',
    'OperateApp.apps.OperateappConfig',
    'rest_framework.apps.RestFrameworkConfig',
    'django_filters',
    'rest_framework_simplejwt',
    'DjangoUeditor',

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

ROOT_URLCONF = 'IBOOLOO.urls'

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

WSGI_APPLICATION = 'IBOOLOO.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = 'media'
MEDIA_URL = 'media/'
X_FRAME_OPTIONS = 'sameorigin'
AUTH_USER_MODEL = 'UserApp.CustomUser'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ],
    # 配置默认授权
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # 配置默认使用的全局分页类,BasePagination为分页类的基类，
    # PageNumberPagination一个简单的基于页码的样式，支持页码查询参数
    # LimitOffsetPagination基于limit限制/offset偏移量的样式
    # CursorPagination加密分页方式，只能通过点击"上一页"、"下一页"访问数据基于游标的分页
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    # 'rest_framework.pagination.LimitOffsetPagination',
    # 'rest_framework.pagination.CursorPagination',
    # 'CapsuleDiary.pagination.SuperPageNumberPagination',

    'PAGE_SIZE': 5,
    # 配置过滤DEFAULT_FILTER_BACKENDS：默认的过滤器后端
    # SearchFilter搜索，OrderingFilter排序
    # 'DEFAULT_FILTER_BACKENDS': [
    #     'django_filters.rest_framework.DjangoFilterBackend',
    #     'rest_framework.filters.SearchFilter',
    #     'rest_framework.filters.OrderingFilter',
    # ],
    # # 3.限流（防爬虫）
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    # ],
    # # 3.1限流策略
    # 'DEFAULT_THROTTLE_RATES': {
    #     'user': '10000/hour',  # 认证用户每小时100次
    #     'anon': '3000/day',  # 未认证用户每天能访问3次
    # },
}
# 配置自定义身份验证后端rest_framework_swagger 可以仿照venv\Lib\site-packages\django\conf\global_settings.py里配置文件仿写
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',
                           'IBOOLOO.backends.CustomBackend']
# 允许跨域
CORS_ORIGIN_ALLOW_ALL = True
# 发送邮件运营商 Q邮箱 POP3 和 SMTP 服务器地址设置如下：
# 邮箱 POP3服务器（端口995） SMTP服务器（端口465或587）
# qq.com pop.qq.com smtp.qq.com SMTP服务器需要身份验证。
EMAIL_HOST = 'pop.qq.com'
EMAIL_POST = '587'
EMAIL_HOST_USER = 'christopher.nesson@foxmail.com'
EMAIL_HOST_PASSWORD = 'jlendtnilgfdebbc'