from django.urls import path, include

urlpatterns = [
    # Все API-маршруты приложения electronics подключаем отсюда
    path("", include("electronics.api.urls")),
]
