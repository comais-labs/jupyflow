from typing import Any
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-field", "placeholder": "Seu nome de usuário"}
        ),
    )
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-field", "placeholder": "Sua senha"}
        )
    )
