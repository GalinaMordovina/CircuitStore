## Онлайн платформа-торговой сети электроники

### Ветка postgres-settings
#### В рамках данной ветки реализовано подключение проекта к базе данных PostgreSQL.

### Настройка PostgreSQL
#### 1. Создание базы данных

В PostgreSQL создаётся база данных:
```
CREATE DATABASE circuitstore_db;
```
#### 2. Создание пользователя

Создаётся отдельный пользователь для работы приложения:
```
CREATE USER circuitstore_user WITH PASSWORD 'your_password';
```
#### 3. Выдача прав пользователю

Пользователь получает права на работу с базой данных:
```
GRANT ALL PRIVILEGES ON DATABASE circuitstore_db TO circuitstore_user;
```
Это позволяет:
- читать данные
- создавать таблицы
- изменять таблицы
- использовать базу данных для тестирования

#### 4. Настройка подключения в Django

В `config/settings.py` используется подключение:
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "circuitstore_db",
        "USER": "circuitstore_user",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```
#### 5. Применение миграций

После подключения базы данных выполняются миграции:
```
python manage.py migrate
```
Это создаёт все таблицы проекта.

#### 6. Создание администратора
```
python manage.py createsuperuser
```
После этого можно работать через Django Admin:
```
http://127.0.0.1:8000/admin/
```

### Проверка работы базы данных

В проекте реализована модель сети поставок электроники:

- Factory - завод
- Retail - розничная сеть
- Entrepreneur - магазин

Пример структуры сети:

Apple Factory

    ↓
Apple Retail

    ↓
Local Electronics Shop

И аналогично для Samsung.

#### Данные сохраняются в PostgreSQL и могут быть проверены SQL-запросом:
```
SELECT 
n.name AS node,
p.name AS product,
p.model AS model
FROM electronics_networknode_products np
JOIN electronics_networknode n ON np.networknode_id = n.id
JOIN electronics_product p ON np.product_id = p.id
ORDER BY n.name;
```
