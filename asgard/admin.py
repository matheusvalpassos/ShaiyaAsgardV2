from django.contrib import admin
from .models import NewsUpdate, ServerStatus
from django.utils.html import format_html


@admin.register(NewsUpdate)
class NewsUpdateAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "label", "is_active", "preview_image")
    list_editable = ("is_active",)
    list_filter = ("label", "is_active")
    search_fields = ("title", "content")
    ordering = ("-published_date",)

    fieldsets = (
        ("Conteúdo", {"fields": ("title", "content", "image", "label")}),
        ("Configurações", {"fields": ("redirect_link", "is_active", "published_date")}),
    )

    @admin.display(description="Imagem")
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" width="80" height="40" style="object-fit:cover;" />'
            )
        return "-"


@admin.register(ServerStatus)
class ServerStatusAdmin(admin.ModelAdmin):
    list_display = ("is_online", "last_updated")
    readonly_fields = ("last_updated",)

    def has_add_permission(self, request):
        return not ServerStatus.objects.exists()

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("id")[:1]
