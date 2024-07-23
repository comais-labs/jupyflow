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
    path("criar", login_required(TurmasCreateView.as_view()), name="criar"),
    path("<int:pk>",  login_required(TurmaDetailView.as_view()), name="ver"),
    path("<int:pk>/editar",  login_required(TurmasUpdateView.as_view()), name="editar"),
    path("<int:pk>/deletar",  login_required(turma_delete_view), name="deletar"),
    path("<int:pk>/aluno/criar",  login_required(AlunoCreateView.as_view()), name="aluno_criar"),
    path(
        "<int:pk_turma>/aluno/<int:pk_aluno>/editar",
        login_required(AlunoUpdateView.as_view()),
        name="aluno_editar",
    ),
    path(
        "<int:pk>/container/start",
        login_required(ContainerStartView.as_view()),
        name="subir_container",
    ),
    path(
        "<int:pk>/documento",
        login_required(PostarDocumentoView.as_view()),
        name="postar_documento",
    ),
]
