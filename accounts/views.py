from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

from .forms import RegistrationForm

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')  # Substitua pelo nome da sua URL de sucesso
    
    def form_valid(self, form):
        # Criar o usuário
        user = form.save()
        
        # Mostrar mensagem de sucesso
        messages.success(self.request, 'Registro realizado com sucesso! Você pode fazer login agora.')
        
        # Redirecionar para a página de login
        return redirect('home')  # Substitua pelo nome da sua URL de login
        
    def form_invalid(self, form):
        # Mostrar mensagens de erro
        for field in form.errors:
            for error in form.errors[field]:
                messages.error(self.request, error)
                
        return super().form_invalid(form)