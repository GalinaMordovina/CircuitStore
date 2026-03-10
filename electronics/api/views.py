from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from electronics.api.permissions import IsActiveStaffPermission
from electronics.api.serializers import NetworkNodeSerializer
from electronics.models import NetworkNode


@extend_schema(
    summary="Проверка доступности API",
    description="Публичная точка доступа для проверки состояния API.",
    responses={200: OpenApiTypes.OBJECT},
)
class HealthCheckView(APIView):
    """Простая проверка, что API работает."""

    # Делаем этот эндпоинт публичным (даже если API закрыт авторизацией)
    permission_classes = [AllowAny]

    def get(self, request):
        # Возвращаем простой ответ для проверки работоспособности API
        return Response({"status": "ok"})


@extend_schema_view(
    list=extend_schema(
        summary="Получить список звеньев сети",
        description=(
            "Возвращает список звеньев сети электроники. "
            "Поддерживается фильтрация по стране, поиск и сортировка."
        ),
        parameters=[
            OpenApiParameter(
                name="country",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Фильтрация по стране, например Germany",
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Поиск по названию, городу, стране и email",
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Сортировка по name, created_at, country, city, hierarchy_level",
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Получить одно звено сети",
        description="Возвращает подробную информацию по одному звену сети.",
    ),
    create=extend_schema(
        summary="Создать звено сети",
        description="Создает новое звено сети электроники.",
    ),
    update=extend_schema(
        summary="Полностью обновить звено сети",
        description="Полностью обновляет данные звена сети.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить звено сети",
        description="Частично обновляет данные звена сети.",
    ),
    destroy=extend_schema(
        summary="Удалить звено сети",
        description="Удаляет звено сети из системы.",
    ),
)
class NetworkNodeViewSet(viewsets.ModelViewSet):
    """CRUD для звеньев сети."""

    queryset = NetworkNode.objects.select_related("supplier").prefetch_related("products")
    serializer_class = NetworkNodeSerializer

    # Доступ только для активных сотрудников
    permission_classes = [IsActiveStaffPermission]

    # Подключаем фильтрацию, поиск и сортировку
    filter_backends = [
        DjangoFilterBackend,  # фильтрация по точным значениям полей
        SearchFilter,  # поиск по текстовым полям
        OrderingFilter,  # сортировка по указанным полям
    ]

    # По ТЗ нужна фильтрация по стране
    filterset_fields = ("country",)

    # Поля, по которым будет работать поиск ?search=
    search_fields = (
        "name",
        "city",
        "country",
        "email",
    )

    # Поля, по которым можно сортировать через ?ordering=
    ordering_fields = (
        "name",
        "created_at",
        "country",
        "city",
        "hierarchy_level",
    )

    # Сортировка по умолчанию
    ordering = ("name",)
