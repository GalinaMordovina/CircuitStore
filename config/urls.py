from django.contrib import admin
from django.urls import path, include

# Готовые view для получения и обновления JWT-токенов
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Токен доступа и refresh-токен
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/", include("electronics.urls")),
]
