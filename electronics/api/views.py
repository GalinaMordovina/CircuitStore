from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from electronics.api.permissions import IsActiveStaffPermission
from electronics.api.serializers import NetworkNodeSerializer
from electronics.models import NetworkNode


class HealthCheckView(APIView):
    """Простая проверка, что API работает."""

    # Делаем этот эндпоинт публичным (даже если API закрыт авторизацией)
    permission_classes = [AllowAny]

    def get(self, request):
        # Возвращаем простой ответ для проверки работоспособности API
        return Response({"status": "ok"})


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
