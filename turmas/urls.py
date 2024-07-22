from django.urls import path
from django.contrib.auth.decorators import login_required

from turmas.views import (
    TurmasCreateView,
    TurmasIndexView,
    TurmaDetailView,
    AlunoCreateView,
    AlunoUpdateView,
    ContainerStartView,
    TurmasUpdateView,
)

app_name = "turmas"

urlpatterns = [
    path("", login_required(TurmasIndexView.as_view()), name="index"),
    path("turmas/criar", login_required(TurmasCreateView.as_view()), name="criar"),
    path("turmas/<int:pk>",  login_required(TurmaDetailView.as_view()), name="ver"),
    path("turmas/<int:pk>/editar",  login_required(TurmasUpdateView.as_view()), name="editar"),
    path("turmas/<int:pk>/aluno/criar",  login_required(AlunoCreateView.as_view()), name="aluno_criar"),
    path(
        "turmas/<int:pk_turma>/aluno/<int:pk_aluno>/editar",
        login_required(AlunoUpdateView.as_view()),
        name="aluno_editar",
    ),
    path(
        "turmas/<int:pk>/container/start",
        login_required(ContainerStartView.as_view()),
        name="subir_container",
    ),
]
