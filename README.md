## Онлайн платформа-торговой сети электроники

### ## Ветка auth-and-access-check

### ## Аутентификация и контроль доступа

В проекте реализована аутентификация пользователей с использованием JWT-токенов и разграничение доступа к API.

### JWT-аутентификация

Для аутентификации используется библиотека `djangorestframework-simplejwt`.

#### Добавлены эндпоинты:

| Метод | URL | Описание |
|------|-----|-----|
| POST | `/api/token/` | Получение access и refresh токенов |
| POST | `/api/token/refresh/` | Обновление access токена |

#### Пример запроса:

```json
POST /api/token/

{
  "username": "staff_user",
  "password": "password"
}
```
Ответ:
```json
{
  "refresh": "jwt_refresh_token",
  "access": "jwt_access_token"
}
```
#### Использование токена

Для доступа к защищённым эндпоинтам необходимо передать access-токен в заголовке запроса:

```Authorization: Bearer <access_token>```

Пример:
```
GET /api/network-nodes/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
#### Ограничение доступа

Для защиты API реализован кастомный permission-класс:

``` IsActiveStaffPermission ```

Доступ к API имеют только пользователи, которые:
- авторизованы
- имеют статус сотрудника (`is_staff=True`)
- имеют активную учетную запись (`is_active=True`)

Данный permission применяется к ViewSet:
```NetworkNodeViewSet```

#### Проверка прав доступа

Была выполнена проверка работы системы доступа с использованием трёх типов пользователей:

| Пользователь   | is_staff | is_active | Результат           |
| -------------- | -------- | --------- | ------------------- |
| staff_user     | True     | True      | полный доступ к API |
| regular_user   | False    | True      | доступ запрещён     |
| inactive_staff | True     | False     | токен не выдаётся   |

Таким образом доступ к API получают только активные сотрудники системы, что соответствует требованиям задания.
