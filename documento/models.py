import os
from django.db import models

from turmas.models import Turma


def upload_documento(instance: "Documento", filename: str):
    tipo = os.path.splitext(filename)[-1].split(".")[-1]
    store_name = f"{instance.nome}.{tipo}"
    return f"documentos/{instance.turma.container.nome_container}/{store_name}"


class Documento(models.Model):
    nome = models.CharField("Nome do documento", max_length=100, null=False)
    documento = models.FileField(upload_to=upload_documento)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=False)
