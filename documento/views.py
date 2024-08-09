from django.shortcuts import render
from django.urls import reverse_lazy

from ansible.manager import AnsibleManager
from base.settings import BASE_DIR
from documento.forms import DocumentoCreateForm
from documento.utils import upload_file_to_server
from turmas.models import Aluno, Turma

from django.db import transaction
from django.views.generic.edit import FormView


# Create your views here.
class PostarDocumentoView(FormView):
    template_name = "turmas/documento_create.html"
    form_class = DocumentoCreateForm

    @transaction.atomic
    def form_valid(self, form):
        turma = Turma.objects.filter(id=self.kwargs["pk"]).first()
        if turma:
            form.instance.turma = turma
        form.save()

        path_documento = f"{str(BASE_DIR)}/{form.instance.documento.name}"
        nome_documento = path_documento.split("/")[-1]
        alunos_nome = [
            str(aluno)
            for aluno in Aluno.objects.filter(turma=turma).values_list(
                "nome", flat=True
            )
        ]
        nome_container = turma.container.nome_container
        upload_file_to_server(file_path=path_documento, document_name=nome_documento)

        ansible_manager = AnsibleManager()
        ansible_manager.upload_file_container(
            nome_container=nome_container,
            nome_documento=nome_documento,
            alunos=alunos_nome,
            path_documento=path_documento,
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("turmas:ver", kwargs={"pk": self.kwargs["pk"]})
