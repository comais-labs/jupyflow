from typing import Any
from django import forms

from google_api.api import GoogleAPI
from turmas.models import ContainerTurma, Turma, Aluno, get_porta_default, UltimaPorta
from ansible.manager import AnsibleManager

google_api = GoogleAPI()


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        exclude = ["alunos", "container"]

    def __init__(self, *args, **kwargs):
        super(TurmaForm, self).__init__(*args, **kwargs)

        formularios = [("0", "Nenhum")]
        formularios.extend(
            [
                (formulario["id"], formulario["name"])
                for formulario in google_api.get_formularios_inscricao()
            ]
        )

        FORMULARIOS = formularios

        self.fields["nome_curso"].widget = forms.TextInput(
            attrs={"class": "form-field"}
        )

        self.fields["nome_turma"].widget = forms.TextInput(
            attrs={"class": "form-field"}
        )

        self.fields["nome_container"] = forms.CharField(
            label="Nome do container",
            max_length=20,
            required=True,
            widget=forms.TextInput(attrs={"class": "form-field"}),
        )
        self.fields["lista_alunos"] = forms.CharField(
            label="Lista de alunos",
            required=False,
            widget=forms.TextInput(attrs={"class": "form-field"}),
        )
        self.fields["formulario"] = forms.ChoiceField(
            label="Formulários",
            choices=FORMULARIOS,
            widget=forms.Select(attrs={"class": "form-select"}),
            required=False,
        )
        self.fields["porta"] = forms.CharField(
            label="Porta do container",
            required=False,
            widget=forms.TextInput(
                attrs={"class": "form-field", "placeholder": get_porta_default()}
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        lista_alunos = cleaned_data.get("lista_alunos")
        formulario = cleaned_data.get("formulario")

        if not lista_alunos and not formulario:
            self.add_error("lista_alunos", "Escolha a lista de alunos da turma")
            self.add_error("formulario", "Escolha a lista de alunos da turma")

        return cleaned_data

    def clean_nome_container(self):
        nome_container = self.cleaned_data.get("nome_container")
        if not nome_container:
            self.add_error(
                "nome_container", "O nome do container não pode estar vazio."
            )

        if " " in nome_container:
            self.add_error(
                "nome_container", "Não podem haver espaços no nome do container"
            )

        return nome_container

    def clean_porta(self):
        porta = self.cleaned_data.get("porta")
        if not porta:
            porta = get_porta_default()

        return porta

    def save(self, commit=True) -> Any:
        instance = super().save(commit=False)

        if commit == True:
            instance.save()

        return instance


class TurmaUpdateForm(TurmaForm):
    def __init__(self, *args, **kwargs):
        super(TurmaUpdateForm, self).__init__(*args, **kwargs)

        self.fields["nome_container"] = forms.CharField(
            label="Nome do container",
            max_length=20,
            required=True,
            initial=self.instance.container.nome_container,
            widget=forms.TextInput(attrs={"class": "form-field"}),
        )
        self.fields["porta"] = forms.CharField(
            label="Porta do container",
            required=False,
            initial=self.instance.container.porta,
            widget=forms.TextInput(attrs={"class": "form-field"}),
        )


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ["turma"]

    def __init__(self, *args, **kwargs):
        super(AlunoForm, self).__init__(*args, **kwargs)
        self.fields["nome"].widget = forms.TextInput(attrs={"class": "form-field"})
        self.fields["senha"].widget = forms.TextInput(attrs={"class": "form-field"})


class AlunoCreateForm(AlunoForm):
    def save(self, commit=True) -> Aluno:
        instance = super().save()
        if commit:
            instance.save()
        return instance
