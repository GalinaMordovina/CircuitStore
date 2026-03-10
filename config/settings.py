from pathlib import Path
import os
from datetime import timedelta

from dotenv import load_dotenv


# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent
# Загружаем переменные окружения из файла .env
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv('SECRET_KEY')

# Режим отладки:
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Список разрешённых хостов
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # сторонние
    "rest_framework",
    "django_filters",
    "drf_yasg",
        "rest_framework_simplejwt",  # JWT-аутентификация

    # наши приложения
    "electronics",
]

# Middleware (промежуточные слои)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основной файл маршрутизации
ROOT_URLCONF = 'config.urls'

# Шаблоны
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

# Точка входа WSGI
WSGI_APPLICATION = 'config.wsgi.application'


# База данных PostgreSQL
DATABASES = {
    "default": {
        # PostgreSQL вместо SQLite
        "ENGINE": "django.db.backends.postgresql",

        # Название базы данных
        "NAME": os.getenv("POSTGRES_DB"),

        # Пользователь PostgreSQL
        "USER": os.getenv("POSTGRES_USER"),

        # Пароль пользователя PostgreSQL
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),

        # Хост, где запущена база данных
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),

        # Порт PostgreSQL
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}


# Валидация паролей
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Локализация
LANGUAGE_CODE = 'ru'         # язык интерфейса

TIME_ZONE = 'Europe/Moscow'  # часовой пояс

USE_I18N = True

USE_TZ = True


# Статические и медиа-файлы
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static",]

# Это настройка Django, которая определяет тип поля первичного ключа (id),
# создаваемого по умолчанию для всех моделей, если я явно не указала id в модели.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    # По умолчанию доступ только у авторизованных пользователей
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    # Используем JWT для аутентификации
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],

    # Глобальный backend для фильтрации
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

# Настройки JWT-токенов
SIMPLE_JWT = {
    # Увеличиваем время жизни access-токена для удобства тестирования
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),

    # Refresh-токен живет дольше
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
