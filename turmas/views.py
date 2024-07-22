import codecs
from typing import Any
from django.forms.models import BaseModelForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, UpdateView

from ansible import manager
from google_api.api import GoogleAPI
from turmas.forms import TurmaForm, AlunoForm, TurmaUpdateForm
from turmas.models import ContainerTurma, Turma, Aluno, UltimaPorta
from ansible.manager import AnsibleManager


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

    def _get_lista_alunos_formulario(self):
        google_api = GoogleAPI()
        formulario_id = self.request.POST.get("formulario")
        if formulario_id != "0":
            _, email_question_id = google_api.get_formulario_email_question_id(
                formulario_id
            )
            lista_emails = google_api.get_lista_email_alunos(
                formulario_id, email_question_id
            )
            if lista_emails:
                return [
                    aluno[: aluno.index("@")].replace(".", "").lower()
                    for aluno in lista_emails
                ]
        return []

    def _get_lista_alunos_manual(self):
        lista_alunos = self.request.POST.get("lista_alunos")
        if lista_alunos:
            return [
                aluno[: aluno.index("@")].replace(".", "").lower()
                for aluno in lista_alunos.split()
            ]
        return []

    def form_valid(self, form):
        instance = form.save()
        container = ContainerTurma.objects.create(
            nome_container=form.cleaned_data.get("nome_container"),
            porta=form.cleaned_data.get("porta"),
        )

        alunos = self._get_lista_alunos_formulario()
        if not alunos:
            alunos = self._get_lista_alunos_manual()

        for aluno in alunos:
            Aluno.objects.create(
                nome=aluno,
                senha=aluno,
                turma=instance,
            )

        instance.container = container
        instance.save()

        ultima_porta = UltimaPorta.objects.first()
        if ultima_porta:
            ultima_porta.ultima_porta = str(int(ultima_porta.ultima_porta) + 1)
            ultima_porta.save()
        else:
            ultima_porta = UltimaPorta.objects.create(
                ultima_porta=8000
            )

        print("Criando container...")
        ansible_manager = AnsibleManager(container=container)
        ansible_manager.setup_container(alunos=alunos, turmas=Turma.objects.all())

        return super().form_valid(form)


class TurmasUpdateView(UpdateView):
    template_name = "turmas/turma_create.html"
    form_class = TurmaUpdateForm
    model = Turma

    def get_success_url(self) -> str:
        return reverse_lazy("turmas:ver", kwargs={"pk": self.kwargs["pk"]})


class AlunoCreateView(FormView):
    template_name = "turmas/aluno_create.html"
    form_class = AlunoForm

    def form_valid(self, form):
        try:
            instance = form.save(commit=False)
            turma = Turma.objects.filter(pk=self.kwargs["pk"]).first()

            ansible_manager = manager.AnsibleManager(container=turma.container)
            ansible_manager.adicionar_alunos_container([instance.nome])

            instance.turma = turma
            instance.save()
        except Exception as error:
            print(error)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("turmas:ver", kwargs={"pk": self.kwargs["pk"]})


class AlunoUpdateView(UpdateView):
    template_name = "turmas/aluno_create.html"
    form_class = AlunoForm
    model = Aluno

    def get_object(self, queryset=None):
        return Aluno.objects.filter(pk=self.kwargs["pk_aluno"]).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy("turmas:ver", kwargs={"pk": self.kwargs["pk_turma"]})


class TurmaDetailView(DetailView):
    template_name = "turmas/turma_detail.html"
    model = Turma

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        alunos = Aluno.objects.filter(turma=self.object)
        context["alunos"] = alunos

        container = ContainerTurma.objects.filter(turma=self.object).first()
        if container and container.ansible_log:
            context["ansible_log"] = codecs.decode(
                container.ansible_log, "unicode_escape"
            )
        return context


class ContainerStartView(DetailView):
    template_name = "turmas/container_run.html"
    model = ContainerTurma

    def post(self, request, *args, **kwargs):
        container = ContainerTurma.objects.filter(turma=self.kwargs["pk"]).first()
        alunos = Aluno.objects.filter(turma_id=self.kwargs["pk"])

        lista_alunos = []
        for aluno in alunos:
            lista_alunos.append(aluno.nome)

        if container:
            ansible_manager = AnsibleManager(container=container)
            ansible_manager.setup_container(
                turmas=Turma.objects.all(), alunos=lista_alunos
            )

        return redirect(reverse_lazy("turmas:ver", kwargs={"pk": self.kwargs["pk"]}))
