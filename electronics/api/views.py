from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Простая проверка, что API работает."""

    def get(self, request):
        # Возвращаем простой ответ для проверки работоспособности API
        return Response({"status": "ok"})
