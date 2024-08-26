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
    success_url = reverse_lazy("turmas:index")

    def form_valid(self, form):
        usuario = form.get_user()
        login(self.request, usuario)
        return super().form_valid(form)


def logout_user_view(request):
    if request.method == "POST":
        logout(request)
        return redirect(reverse_lazy("usuario:login"))
