from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-field", "placeholder": "Seu nome de usuário"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-field", "placeholder": "Sua senha"}
        )
    )

    def get_user(self):
        return self.user

    def clean(self) -> dict[str, Any]:
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        self.user = authenticate(username=username, password=password)
        if not self.user:
            raise forms.ValidationError("Usuário ou senha estão incorretos")

        return self.cleaned_data
