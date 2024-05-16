from typing import Any
from django import forms

from turmas.models import ContainerTurma, Turma

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        exclude = ['alunos', 'container']

    def __init__(self, *args, **kwargs):
        super(TurmaForm, self).__init__(*args, **kwargs)
        self.fields['nome_container'] = forms.CharField(label="Nome do container", max_length=20, required=True)
        self.fields['lista_alunos'] = forms.CharField(label="Lista de alunos", required=True)

    def clean_lista_alunos(self):
        lista_alunos = self.cleaned_data.get('lista_alunos')
        if not lista_alunos:
            raise forms.ValidationError("A lista de alunos não pode estar vazia")

        lista_alunos = lista_alunos.split(' ')
        return lista_alunos
        

    def save(self, commit=True) -> Any:
        instance = super().save(commit=False)
        instance.alunos = self.cleaned_data.get('lista_alunos')

        container = ContainerTurma.objects.create(
            nome_container=self.cleaned_data.get('nome_container'),
        )

        instance.container = container

        if commit == True:
            instance.save()

        return instance