import json
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render # <-- ADICIONE 'render' AQUI
from django.http import JsonResponse

from .forms import RegistrationForm


class RegisterView(FormView):
    template_name = "accounts/register.html"  # Este template será usado para GET requests (carregar o formulário)
    form_class = RegistrationForm
    success_url = reverse_lazy("home")  # Substitua pelo nome da sua URL de sucesso

    def form_valid(self, form):
        user = form.save()

        # Verifica se é uma requisição AJAX
        if self.request.headers.get(
            "x-requested-with"
        ) == "XMLHttpRequest" or self.request.accepts("application/json"):
            return JsonResponse(
                {
                    "message": "Registro realizado com sucesso!",
                    "username": user.username,
                },
                status=201,
            )

        # Comportamento padrão (não-AJAX): mostra mensagem e redireciona
        messages.success(
            self.request, "Registro realizado com sucesso! Você pode fazer login agora."
        )
        return redirect(self.success_url)  # Usar self.success_url para redirecionar

    def form_invalid(self, form):
        # Verifica se é uma requisição AJAX
        if self.request.headers.get(
            "x-requested-with"
        ) == "XMLHttpRequest" or self.request.accepts("application/json"):
            errors = {field: list(errors) for field, errors in form.errors.items()}
            return JsonResponse(
                {"error": "Erro de validação", "details": errors}, status=400
            )

        # Comportamento padrão (não-AJAX): mostra mensagens de erro e renderiza o formulário
        for field in form.errors:
            for error in form.errors[field]:
                messages.error(self.request, error)

        return super().form_invalid(
            form
        )  # Isso irá renderizar o template com o formulário e os erros


# --- Nova view para servir o fragmento HTML do formulário de registro via GET ---
# O seu spa.js fará um GET para uma URL mapeada para esta view para obter o HTML do formulário.
def register_form_html_view(request):
    form = RegistrationForm()  # Cria uma instância vazia do formulário
    return render(
        request, "accounts/register.html", {"form": form}
    )  # Renderiza o template com o formulário
