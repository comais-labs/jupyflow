from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout

from usuario.forms import LoginForm

# Create your views here.


class LoginView(FormView):
    template_name = "usuario/login.html"
    form_class = LoginForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        username = request.POST.get("username")
        password = request.POST.get("password")
        usuario = authenticate(request, username=username, password=password)
        if usuario:
            login(request, usuario)
            return redirect(reverse_lazy("turmas:index"))
        else:
            return super().post(request, *args, **kwargs)

def logout_user_view(request):
    if request.method == "POST":
        logout(request)
        return redirect(reverse_lazy("usuario:login"))
