## Онлайн платформа-торговой сети электроники

### Технологии
- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- drf-yasg
- django-filter

## Что сделано в ветке feature/init-project
- создан Django-проект CircuitStore
- создано приложение electronics
- подключены базовые зависимости
- настроено чтение переменных окружения через `.env`
- добавлен `.env.example`
- подготовлен базовый `README`
- выполнены стартовые настройки проекта

## Запуск проекта локально
1. Создать и активировать виртуальное окружение
2. Установить зависимости:
   ```bash
   pip install -r requirements.txt

3. Создать .env на основе .env.example
4. Применить миграции:
    ```bash
   python manage.py migrate
5. Запустить сервер:
    ```bash
   python manage.py runserver
   