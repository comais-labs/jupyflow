from django import forms

from documento.models import Diretorio, Documento
from turmas.models import Turma


class DocumentoCreateForm(forms.ModelForm):
    class Meta:
        model = Documento
        exclude = ["turma"]

    def __init__(self, *args, **kwargs):
        super(DocumentoCreateForm, self).__init__(*args, **kwargs)

        self.fields["nome"].widget = forms.TextInput(attrs={"class": "form-field"})
        self.fields["documento"].widget = forms.FileInput(
            attrs={"class": "form-file-field"}
        )

    def save(self, commit=True) -> Documento:
        instance = super().save()
        if commit:
            instance.save()
        return instance


class DocumentosVariasTurmasCreateForm(DocumentoCreateForm):
    def __init__(self, *args, **kwargs):
        super(DocumentosVariasTurmasCreateForm, self).__init__(*args, **kwargs)
        TURMAS = [(turma.id, turma.nome) for turma in Turma.objects.all()]
        self.fields["turmas"] = forms.ChoiceField(
            choices=TURMAS, widget=forms.CheckboxSelectMultiple()
        )

    def clean_turmas(self):
        turmas = self.cleaned_data.get("turmas")
        if not turmas:
            raise forms.ValidationError("Você deve selecionar pelo menos uma turma")


class DiretorioCreateForm(forms.ModelForm):
    class Meta:
        model = Diretorio
        exclude = ["container"]

    def __init__(self, *args, **kwargs):
        super(DiretorioCreateForm, self).__init__(*args, **kwargs)
        self.fields["pai"] = forms.ChoiceField(choices=Diretorio.objects.all())
