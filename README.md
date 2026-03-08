## Онлайн платформа-торговой сети электроники

### ## Ветка feature/api-crud-permissions

### Реализовано:

- добавлен API для модели звеньев сети на DRF;
- реализован NetworkNodeViewSet с CRUD-операциями;
- настроена фильтрация по стране через django-filter;
- доступ к API разрешен только активным сотрудникам (is_active=True и is_staff=True);
- поле debt_to_supplier запрещено изменять через API;
- поля hierarchy_level и created_at доступны только для чтения;
- добавлен служебный эндпоинт проверки API: /api/health/.

### Проверка API
#### Доступные маршруты
- GET /api/health/ - проверка работоспособности API
- GET /api/network-nodes/ - список звеньев сети
- POST /api/network-nodes/ - создание звена сети
- GET /api/network-nodes/<id>/ - получение одного объекта
- PUT /api/network-nodes/<id>/ - полное обновление
- PATCH /api/network-nodes/<id>/ - частичное обновление
- DELETE /api/network-nodes/<id>/ - удаление объекта

#### Фильтрация
- по стране:/api/network-nodes/?country=Germany

#### Ограничения API
Через API запрещено изменять поля:
- debt_to_supplier
- hierarchy_level
- created_at
