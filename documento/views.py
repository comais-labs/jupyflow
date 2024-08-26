from django.shortcuts import render
from django.urls import reverse_lazy

from ansible.manager import AnsibleManager
from base.settings import BASE_DIR
from documento.forms import (
    DiretorioCreateForm,
    DocumentoCreateForm,
    DocumentosVariasTurmasCreateForm,
)
from documento.models import Documento
from documento.utils import upload_file_to_server
from turmas.models import Aluno, Turma

from django.db import transaction
from django.views.generic.edit import FormView


class PostarDocumentoView(FormView):
    template_name = "turmas/documento_create.html"
    form_class = DocumentoCreateForm

    @transaction.atomic
    def form_valid(self, form):
        turma = Turma.objects.filter(id=self.kwargs["pk"]).first()
        Documento.objects.create_in_container(turma=turma, documento=form.instance)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("turmas:ver", kwargs={"pk": self.kwargs["pk"]})


class PostarDocumentoVariasTurmasView(FormView):
    template_name = "turmas/documentos_create.html"
    form_class = DocumentosVariasTurmasCreateForm
    success_url = reverse_lazy("turmas:index")

    @transaction.atomic()
    def form_valid(self, form):
        turmas = self.request.POST.get("turmas")

        form
        return super().form_valid(form)


class CriarDiretorioView(FormView):
    template_name = "turmas/documento_create.html"
    form_class = DiretorioCreateForm
