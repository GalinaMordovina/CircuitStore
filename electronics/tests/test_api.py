import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from electronics.models import NetworkNode, Product


User = get_user_model()


@pytest.fixture
def api_client():
    """Базовый API-клиент для запросов."""
    return APIClient()


@pytest.fixture
def product_iphone(db):
    """Продукт Apple."""
    return Product.objects.create(
        name="iPhone",
        model="15 Pro",
        release_date="2023-09-12",
    )


@pytest.fixture
def product_galaxy(db):
    """Продукт Samsung."""
    return Product.objects.create(
        name="Galaxy",
        model="S24",
        release_date="2024-01-17",
    )


@pytest.fixture
def network_data(db, product_iphone, product_galaxy):
    """Тестовые звенья сети для фильтрации, поиска и сортировки."""

    apple_factory = NetworkNode.objects.create(
        name="Apple Factory",
        node_type="factory",
        email="factory@apple.com",
        country="China",
        city="Shenzhen",
        street="Tech Street",
        house_number="1",
        supplier=None,
        debt_to_supplier="0.00",
    )
    apple_factory.products.add(product_iphone)

    apple_retail = NetworkNode.objects.create(
        name="Apple Retail",
        node_type="retail",
        email="retail@apple.com",
        country="Germany",
        city="Berlin",
        street="Market Street",
        house_number="10",
        supplier=apple_factory,
        debt_to_supplier="1500.00",
    )
    apple_retail.products.add(product_iphone)

    samsung_factory = NetworkNode.objects.create(
        name="Samsung Factory",
        node_type="factory",
        email="factory@samsung.com",
        country="South Korea",
        city="Seoul",
        street="Digital Street",
        house_number="1",
        supplier=None,
        debt_to_supplier="0.00",
    )
    samsung_factory.products.add(product_galaxy)

    samsung_retail = NetworkNode.objects.create(
        name="Samsung Retail",
        node_type="retail",
        email="retail@samsung.com",
        country="Germany",
        city="Berlin",
        street="Shop Street",
        house_number="20",
        supplier=samsung_factory,
        debt_to_supplier="3000.00",
    )
    samsung_retail.products.add(product_galaxy)

    return {
        "apple_factory": apple_factory,
        "apple_retail": apple_retail,
        "samsung_factory": samsung_factory,
        "samsung_retail": samsung_retail,
    }


@pytest.fixture
def staff_user(db):
    """Активный сотрудник с доступом к API."""
    return User.objects.create_user(
        username="staff_user",
        password="Test12345!",
        is_active=True,
        is_staff=True,
    )


@pytest.fixture
def regular_user(db):
    """Активный пользователь без статуса сотрудника."""
    return User.objects.create_user(
        username="regular_user",
        password="Test12345!",
        is_active=True,
        is_staff=False,
    )


@pytest.fixture
def inactive_staff(db):
    """Неактивный сотрудник."""
    return User.objects.create_user(
        username="inactive_staff",
        password="Test12345!",
        is_active=False,
        is_staff=True,
    )


@pytest.fixture
def staff_token(api_client, staff_user):
    """Получаем JWT access token для staff_user."""
    response = api_client.post(
        "/api/token/",
        {"username": "staff_user", "password": "Test12345!"},
        format="json",
    )
    return response.data["access"]


@pytest.mark.django_db
def test_health_endpoint(api_client):
    """Проверяем, что endpoint /api/health/ работает."""
    response = api_client.get("/api/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.django_db
def test_staff_user_can_get_network_nodes(api_client, staff_token, network_data):
    """Активный сотрудник должен иметь доступ к списку звеньев сети."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")

    response = api_client.get("/api/network-nodes/")

    assert response.status_code == 200
    assert len(response.json()) == 4


@pytest.mark.django_db
def test_regular_user_forbidden_for_network_nodes(api_client, regular_user, network_data):
    """Пользователь без is_staff не должен получать доступ к API."""
    token_response = api_client.post(
        "/api/token/",
        {"username": "regular_user", "password": "Test12345!"},
        format="json",
    )
    access_token = token_response.data["access"]

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = api_client.get("/api/network-nodes/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_inactive_staff_cannot_get_token(api_client, inactive_staff):
    """Неактивный сотрудник не должен получать JWT-токен."""
    response = api_client.post(
        "/api/token/",
        {"username": "inactive_staff", "password": "Test12345!"},
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_filter_by_country(api_client, staff_token, network_data):
    """Фильтрация по стране должна возвращать только нужные объекты."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")

    response = api_client.get("/api/network-nodes/?country=Germany")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(item["country"] == "Germany" for item in data)


@pytest.mark.django_db
def test_search_by_name(api_client, staff_token, network_data):
    """Поиск по слову Apple должен возвращать только объекты Apple."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")

    response = api_client.get("/api/network-nodes/?search=Apple")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all("Apple" in item["name"] for item in data)


@pytest.mark.django_db
def test_ordering_by_name(api_client, staff_token, network_data):
    """Сортировка по имени должна работать корректно."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")

    response = api_client.get("/api/network-nodes/?ordering=name")

    assert response.status_code == 200
    data = response.json()

    names = [item["name"] for item in data]
    assert names == sorted(names)


@pytest.mark.django_db
def test_debt_to_supplier_is_read_only(api_client, staff_token, network_data):
    """
    Поле debt_to_supplier не должно изменяться через API.
    """
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")
    retail_node = network_data["apple_retail"]

    old_debt = retail_node.debt_to_supplier

    response = api_client.patch(
        f"/api/network-nodes/{retail_node.id}/",
        {"debt_to_supplier": "99999.99"},
        format="json",
    )

    assert response.status_code == 200

    retail_node.refresh_from_db()
    assert retail_node.debt_to_supplier == old_debt
