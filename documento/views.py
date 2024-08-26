from django.shortcuts import render
from django.urls import reverse_lazy

from documento.forms import (
    DiretorioCreateForm,
    DocumentoCreateForm,
    DocumentosVariasTurmasCreateForm,
)
from documento.models import Documento
from turmas.models import Turma

from django.db import transaction
from django.views.generic.edit import FormView


class PostarDocumentoView(FormView):
    template_name = "turmas/documento_create.html"
    form_class = DocumentoCreateForm

    @transaction.atomic
    def form_valid(self, form):
        turma = Turma.objects.filter(id=self.kwargs["pk"]).first()
        Documento.objects.create_one(turma=turma, documento=form.instance)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("turmas:ver", kwargs={"pk": self.kwargs["pk"]})


class PostarDocumentoVariasTurmasView(FormView):
    template_name = "documento/documentos_create.html"
    form_class = DocumentosVariasTurmasCreateForm
    success_url = reverse_lazy("turmas:index")

    @transaction.atomic()
    def form_valid(self, form):
        nome = self.request.POST.get("nome")
        turmas = self.request.POST.getlist("turmas")
        documento = self.request.FILES.get("documento")

        Documento.objects.create_multiple(nome=nome, turmas=turmas, documento=documento)
        form.save()
        return super().form_valid(form)


class CriarDiretorioView(FormView):
    template_name = "turmas/documento_create.html"
    form_class = DiretorioCreateForm
