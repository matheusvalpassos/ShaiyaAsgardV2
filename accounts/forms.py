from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.core.validators import RegexValidator
import re


class RegistrationForm(forms.Form):
    userid = forms.CharField(
        validators=[
            RegexValidator(
                r"^[a-zA-Z0-9_]+$", "Only letters, numbers and underscores are allowed."
            )
        ],
        label="Login",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "block w-full h-11 pr-5 pl-14 py-2.5 text-base font-normal shadow-xs text-gray-100 bg-transparent border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none",
                "placeholder": "Enter your login",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "block w-full h-11 pr-5 pl-14 py-2.5 text-base font-normal shadow-xs text-gray-100 bg-transparent border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none",
                "placeholder": "email@email.com",
            }
        ),
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full h-11 pr-5 pl-14 py-2.5 text-base font-normal shadow-xs text-gray-100 bg-transparent border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none",
                "placeholder": "Enter your password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full h-11 pr-5 pl-14 py-2.5 text-base font-normal shadow-xs text-gray-100 bg-transparent border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none",
                "placeholder": "Confirm your password",
            }
        ),
    )

    terms = forms.BooleanField(
        label="Eu aceito os termos de uso",
        error_messages={"required": "Você deve aceitar os termos para continuar."},
        widget=forms.CheckboxInput(attrs={"class": "mr-1 leading-tight"}),
    )

    def clean_userid(self):
        userid = self.cleaned_data.get("userid")

        # Verificar se já existe um usuário com esse ID
        if CustomUser.objects.using("user_data").filter(userid=userid).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")

        # Validar caracteres permitidos
        if not re.match(r"^[a-zA-Z0-9_]+$", userid):
            raise forms.ValidationError(
                "O nome de usuário só pode conter letras, números e sublinhados."
            )

        # Verificar comprimento mínimo
        if len(userid) < 4:
            raise forms.ValidationError(
                "O nome de usuário deve ter pelo menos 4 caracteres."
            )

        return userid

    def clean_email(self):
        email = self.cleaned_data.get("email")

        # Verificar se já existe um usuário com esse email
        if CustomUser.objects.using("user_data").filter(email=email).exists():
            raise forms.ValidationError("Este email já está registrado.")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        # Verificar complexidade da senha
        if len(password1) < 8:
            raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")

        # Você pode adicionar mais validações de senha aqui

        return password2

    def save(self):
        userid = self.cleaned_data.get("userid")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")

        user = CustomUser(
            userid=userid,
            email=email,
            pw=password,  # Texto puro, conforme seu uso
            enpassword=make_password(password),  # Hasheado
            status=0,
            usertype=0,
            admin=False,
            adminlevel=0,
        )
        user.save(using="user_data")
        return user
