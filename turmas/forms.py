from typing import Any
from django import forms

from google_api.api import GoogleAPI
from turmas.models import ContainerTurma, Turma

google_api = GoogleAPI()

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        exclude = ['alunos', 'container']

    def __init__(self, *args, **kwargs):
        super(TurmaForm, self).__init__(*args, **kwargs)

        formularios =[('0', 'Nenhum')]
        formularios.extend([
            (formulario['id'], formulario['name']) 
            for formulario in google_api.get_formularios_inscricao()
        ])

        FORMULARIOS = formularios

        self.fields['nome_container'] = forms.CharField(label="Nome do container", max_length=20, required=True)
        self.fields['lista_alunos'] = forms.CharField(label="Lista de alunos", required=False)
        self.fields['formulario'] = forms.ChoiceField(label="Formulários", choices=FORMULARIOS, widget=forms.Select(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        lista_alunos = cleaned_data.get('lista_alunos')
        formulario = cleaned_data.get('formulario')

        if not lista_alunos and not formulario:
            raise forms.ValidationError("Escolha a lista de alunos da turma")

        print('oi')
        formulario_id = self.cleaned_data.get('formulario')
        if formulario_id:
            self._get_lista_alunos_formulario(formulario_id)


        return cleaned_data

    def clean_lista_alunos(self):
        lista_alunos = self.cleaned_data.get('lista_alunos')
        if not lista_alunos:
            raise forms.ValidationError("A lista de alunos não pode estar vazia")

        lista_alunos = lista_alunos.split(' ')
        return lista_alunos

    def clean_nome_container(self):
        nome_container = self.cleaned_data.get('nome_container')
        if not nome_container:
            raise forms.ValidationError("O nome do container não pode estar vazio.")

        if ' ' in nome_container:
            self.add_error('nome_container', "Não podem haver espaços no nome do container")

        return nome_container

    def _get_lista_alunos_formulario(self, formulario_id):
        print(f'formulario id {formulario_id}')
        email_question_id = google_api.get_formulario_email_question_id(formulario_id)
        lista_emails = google_api.get_lista_email_alunos(formulario_id, email_question_id)
        
        if lista_emails:
            lista_alunos = [
                aluno[:aluno.index('@')].replace('.', '').lower()
                for aluno in lista_emails
            ]

            return lista_alunos
        return []


    def save(self, commit=True) -> Any:
        instance = super().save(commit=False)
        
        formulario_id = self.cleaned_data.get('formulario')
        if formulario_id:
            instance.alunos = self._get_lista_alunos_formulario(formulario_id)
            print(instance.alunos)

        # instance.alunos = self.cleaned_data.get('lista_alunos')

        container = ContainerTurma.objects.create(
            nome_container=self.cleaned_data.get('nome_container'),
        )

        instance.container = container

        if commit == True:
            instance.save()

        return instance
