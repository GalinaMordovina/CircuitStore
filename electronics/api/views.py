from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

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

    # Подключаем фильтрацию
    filter_backends = [DjangoFilterBackend]

    # По ТЗ нужна фильтрация по стране
    filterset_fields = ("country",)
