from django.urls import path
from .views import admin_dashboard_view, user_dashboard_view

urlpatterns = [
    path("admin/", admin_dashboard_view, name="admin_dashboard"),
    path("user/", user_dashboard_view, name="user_dashboard"),
]
