# CircuitStore API

Backend-приложение для управления сетью по продаже электроники.  
Проект реализует иерархическую структуру торговой сети с API, административной панелью и автоматической документацией.

Сеть состоит из трёх уровней:

- завод
- розничная сеть
- индивидуальный предприниматель

Каждое звено сети может ссылаться на одного поставщика, формируя иерархию.

---

# Технологии

Проект реализован с использованием:

- Python 3.12
- Django 6
- Django REST Framework
- PostgreSQL
- JWT (SimpleJWT)
- drf-spectacular (Swagger / ReDoc)
- pytest
- pytest-django
- pytest-cov

---

# Функциональность

## Административная панель

В админ-панели реализовано управление объектами сети:

- создание и редактирование звеньев сети
- управление продуктами
- отображение иерархии поставщиков
- фильтрация по городу
- ссылка на поставщика
- admin action для очистки задолженности перед поставщиком

---

## API

Реализован REST API для управления сетью.

Поддерживаются операции:

- получение списка объектов
- получение одного объекта
- создание
- обновление
- удаление

Поле **debt_to_supplier** запрещено для изменения через API.

---

## Фильтрация

Поддерживается фильтрация:
```
/api/network-nodes/?country=Germany
```

---

## Поиск

Поиск по основным текстовым полям:
```
/api/network-nodes/?search=Apple
```
---

## Сортировка

Пример сортировки:
```
/api/network-nodes/?ordering=name
/api/network-nodes/?ordering=-created_at
```

---

# Аутентификация

Используется JWT-аутентификация.

Получение токена:
```
POST /api/token/
```
Обновление токена:
```
POST /api/token/refresh/
```

Доступ к API имеют **только активные сотрудники** (`is_active=True` и `is_staff=True`).

---

# Документация API

Swagger UI:
Swagger UI:  
[http://127.0.0.1:8000/api/docs/swagger/](http://127.0.0.1:8000/api/docs/swagger/)

ReDoc:  
[http://127.0.0.1:8000/api/docs/redoc/](http://127.0.0.1:8000/api/docs/redoc/)

OpenAPI schema:  
[http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

# Тестирование

В проекте реализованы автоматические тесты.

Используемые инструменты:

- pytest
- pytest-django
- pytest-cov

Проверяются:

- JWT аутентификация
- доступ к API
- запрет доступа для не сотрудников
- фильтрация
- поиск
- сортировка
- запрет изменения поля задолженности


---

# Установка проекта

## 1. Клонировать репозиторий
```
git clone https://github.com/GalinaMordovina/CircuitStore
```

Перейти в папку проекта:
```
cd CircuitStore
```

---

## 2. Создать виртуальное окружение
```
python -m venv .venv
```

Активировать:

Windows: `.venv\Scripts\activate`

Linux / Mac: `source .venv/bin/activate`


---

## 3. Установить зависимости
```
pip install -r requirements.txt
```

---

## 4. Настроить переменные окружения

Создать файл `.env` на основе `.env.example`.

---

## 5. Применить миграции
```
python manage.py migrate
```

---

## 6. Создать суперпользователя
```
python manage.py createsuperuser
```

---

## 7. Запустить сервер
```
python manage.py runserver
```

Приложение будет доступно по адресу:
http://127.0.0.1:8000/

---

# Запуск тестов
```
python -m pytest
```

---

# Структура проекта

## Структура проекта

```text
CircuitStore
│
├── config
│   ├── settings.py
│   └── urls.py
│
├── electronics
│   ├── models.py
│   ├── admin.py
│   ├── urls.py
│   ├── api
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── permissions.py
│   │   └── urls.py
│   └── tests
│       ├── __init__.py
│       └── test_api.py
│
├── .env.example
├── manage.py
├── requirements.txt
├── pytest.ini
└── README.md
```

---

# Автор

Мордовина Галина (glukoloid@gmail.com) 

https://github.com/GalinaMordovina
