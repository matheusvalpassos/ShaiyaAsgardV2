from django.urls import path, include
from django.conf.urls.static import static
from .views import home, NewsUpdateView, error_404_view
from django.conf import settings


urlpatterns = [
    path("", home, name="home"),
    path('erro-404/', error_404_view, name='erro-404'),
    path("admin/", include("dashboard.urls")),
    path("", include("accounts.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
