
from django.urls import path

from turmas.views import TurmasCreateView, TurmasIndexView, TurmaDetailView, AlunoCreateView

app_name = "turmas"

urlpatterns = [
    path("", TurmasIndexView.as_view(), name="index"),
    path("turmas/criar", TurmasCreateView.as_view(), name="criar"),
    path("turmas/<int:pk>", TurmaDetailView.as_view(), name="ver"),
    path("turmas/<int:pk>", TurmaDetailView.as_view(), name="ver"),
    path("turmas/<int:pk>/aluno/criar", AlunoCreateView.as_view(), name="aluno_criar"),
]