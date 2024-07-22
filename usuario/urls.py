from django.urls import path

from usuario.views import LoginView, logout_user_view

app_name = "usuario"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login" ),
    path("logout/", logout_user_view, name="logout" ),
]

