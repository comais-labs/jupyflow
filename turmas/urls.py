from django.urls import path

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
    path("", TurmasIndexView.as_view(), name="index"),
    path("turmas/criar", TurmasCreateView.as_view(), name="criar"),
    path("turmas/<int:pk>", TurmaDetailView.as_view(), name="ver"),
    path("turmas/<int:pk>/editar", TurmasUpdateView.as_view(), name="editar"),
    path("turmas/<int:pk>/aluno/criar", AlunoCreateView.as_view(), name="aluno_criar"),
    path(
        "turmas/<int:pk_turma>/aluno/<int:pk_aluno>/editar",
        AlunoUpdateView.as_view(),
        name="aluno_editar",
    ),
    path(
        "turmas/<int:pk>/container/start",
        ContainerStartView.as_view(),
        name="subir_container",
    ),
]
