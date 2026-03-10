## Онлайн платформа-торговой сети электроники

### Ветка api-filters-search

## Фильтрация, поиск и сортировка API

Для endpoint `/api/network-nodes/` реализованы:

- фильтрация по стране
- поиск по названию, городу, стране и email
- сортировка по имени, дате создания, стране, городу и уровню иерархии

### Примеры запросов

Фильтрация по стране:

`GET /api/network-nodes/?country=Germany`

Поиск:

`GET /api/network-nodes/?search=Apple`

Сортировка по имени:

`GET /api/network-nodes/?ordering=name`

Сортировка по дате создания по убыванию:

`GET /api/network-nodes/?ordering=-created_at`
