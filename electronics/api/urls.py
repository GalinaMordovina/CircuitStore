from django.urls import path, include
from rest_framework.routers import DefaultRouter

from electronics.api.views import HealthCheckView, NetworkNodeViewSet


router = DefaultRouter()

router.register("network-nodes", NetworkNodeViewSet, basename="network-nodes")

urlpatterns = [
    # Эндпоинт для проверки, что API поднято
    path("health/", HealthCheckView.as_view(), name="health"),
    path("", include(router.urls)),
]
