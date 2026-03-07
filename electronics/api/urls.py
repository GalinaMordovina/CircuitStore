from django.urls import path

from electronics.api.views import HealthCheckView

urlpatterns = [
    # Эндпоинт для проверки, что API поднято
    path("health/", HealthCheckView.as_view(), name="health"),
]
