from django.contrib import admin

from electronics.models import NetworkNode, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройки админки для продуктов."""

    # Какие поля показывать в списке объектов
    list_display = ("id", "name", "model", "release_date")

    # По каким полям работает поиск
    search_fields = ("name", "model")


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Настройки админки для звеньев сети."""

    # Поля, которые будут видны в таблице админки
    list_display = (
        "id",
        "name",
        "node_type",
        "supplier",
        "city",
        "country",
        "debt_to_supplier",
        "hierarchy_level",
        "created_at",
    )

    # Фильтры справа в админке
    list_filter = ("city", "country", "node_type")

    # Поиск по основным текстовым полям
    search_fields = ("name", "email", "city", "country")

    # Эти поля будут только для чтения в админке
    readonly_fields = ("hierarchy_level", "created_at")
