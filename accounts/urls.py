from django.urls import path
from .views import RegisterView, register_form_html_view  # Importe ambas as views

urlpatterns = [
    # URL para a API de registro (recebe POST do SPA)
    # Ex: /api/register/
    path("api/register/", RegisterView.as_view(), name="register-api"),
    # URL para carregar o fragmento HTML do formulário de registro (recebe GET do SPA)
    # Ex: /register-form/
    path("register-form/", register_form_html_view, name="register-form-html"),
    # Se você tiver uma LoginFormView ou equivalente, faria algo similar:
    # path('api/login/', LoginView.as_view(), name='login-api'),
    # path('login-form/', login_form_html_view, name='login-form-html'),
]
