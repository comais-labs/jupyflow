from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from ansible import setup
from google_api.api import GoogleAPI
from turmas.forms import TurmaForm
from turmas.models import Turma


class TurmasIndexView(TemplateView):
    template_name = "turmas/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["turmas"] = Turma.objects.all()

        google_api = GoogleAPI()

        return context

class TurmasCreateView(FormView):
    template_name = "turmas/turma_create.html"
    form_class = TurmaForm
    success_url = reverse_lazy("turmas:index")

    def form_valid(self, form):
        # form.save()
        nome_container = self.request.POST.get('nome_container')
        alunos = self.request.POST.get('lista_alunos')
        alunos = alunos.split(' ')

        try:
            print('Criando container...')
            # container = setup.ContainerSetup(
            #     container=form.instance.container,
            #     alunos=alunos
            # )
            # container.setup()
        except Exception as error:
            print(error)

        return super().form_valid(form)
    
