from django import forms

from documento.models import Documento


class DocumentoCreateForm(forms.ModelForm):
    class Meta:
        model = Documento
        exclude = ["turma"]

    def __init__(self, *args, **kwargs):
        super(DocumentoCreateForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget = forms.TextInput(attrs={"class":"form-field"})
        self.fields['documento'].widget = forms.FileInput(attrs={"class":"form-file-field"})

    def save(self, commit=True) -> Documento:
        instance = super().save()
        if commit:
            instance.save()
        return instance