from django.urls import path
from django.contrib.auth.decorators import login_required

from turmas.forms import DocumentoCreateForm
from turmas.views import (
    PostarDocumentoView,
    TurmasCreateView,
    TurmasIndexView,
    TurmaDetailView,
    AlunoCreateView,
    AlunoUpdateView,
    ContainerStartView,
    TurmasUpdateView,
    turma_delete_view,
)

app_name = "turmas"

urlpatterns = [
    path("", login_required(TurmasIndexView.as_view()), name="index"),
    path("turmas/criar", login_required(TurmasCreateView.as_view()), name="criar"),
    path("turmas/<int:pk>",  login_required(TurmaDetailView.as_view()), name="ver"),
    path("turmas/<int:pk>/editar",  login_required(TurmasUpdateView.as_view()), name="editar"),
    path("turmas/<int:pk>/deletar",  login_required(turma_delete_view), name="deletar"),
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
    path(
        "turmas/<int:pk>/documento",
        login_required(PostarDocumentoView.as_view()),
        name="postar_documento",
    ),
]
