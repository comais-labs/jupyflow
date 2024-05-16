
from django.urls import path

from turmas.views import TurmasCreateView, TurmasIndexView

app_name = "turmas"

urlpatterns = [
    path("", TurmasIndexView.as_view(), name="index"),
    path("turmas/criar", TurmasCreateView.as_view(), name="criar"),
]