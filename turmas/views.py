from typing import Any
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView

from ansible import setup
from google_api.api import GoogleAPI
from turmas.forms import TurmaForm, AlunoForm
from turmas.models import ContainerTurma, Turma, Aluno





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

    @staticmethod
    def _get_lista_alunos_formulario(formulario_id):
        print(f' view formulario id {formulario_id}')
        google_api = GoogleAPI()
        _, email_question_id = google_api.get_formulario_email_question_id(formulario_id)
        lista_emails = google_api.get_lista_email_alunos(formulario_id, email_question_id)
        if lista_emails:
            lista_alunos = [
                aluno[:aluno.index('@')].replace('.', '').lower()
                for aluno in lista_emails
            ]

            return lista_alunos

        return []

    def form_valid(self, form):
        try:
            instance = form.save()
            alunos = []

            formulario_id = self.request.POST.get("formulario")
            lista_alunos = self.request.POST.get("lista_alunos")

            if formulario_id != '0':
                alunos = self._get_lista_alunos_formulario(formulario_id)
            else:
                alunos = lista_alunos.split(' ')

            for aluno in alunos:

                aluno = Aluno.objects.create(
                    nome=aluno,
                    senha=aluno,
                    turma=instance,
                )
                print(aluno)

            turmas = Turma.objects.all()


            print('Criando container...')
            container = setup.ContainerSetup(
                container=form.instance.container,
                turmas=Turma.objects.all(),
                alunos=alunos
            )
            container.setup()
        except Exception as error:
            print(error)

        return super().form_valid(form)


class AlunoCreateView(FormView):
    template_name = "turmas/aluno_create.html"
    form_class = AlunoForm
class TurmaDetailView(DetailView):
    template_name = "turmas/turma_detail.html"
    context_object_name = 'turma'
    queryset = Turma.objects