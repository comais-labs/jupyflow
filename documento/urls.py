from django.urls import path
from django.contrib.auth.decorators import login_required

from documento.views import PostarDocumentoVariasTurmasView


app_name = "documento"

urlpatterns = [
    path(
        "documento/varias-turmas",
        login_required(PostarDocumentoVariasTurmasView.as_view()),
        name="criar_varios",
    ),
]

