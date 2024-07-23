import hashlib
import os
from django.db import models

# Create your models here.
def get_porta_default():
    ultima_porta = UltimaPorta.objects.first()
    if ultima_porta:
        return int(ultima_porta.ultima_porta) + 1
    return 8000

def upload_documento(instance: "Documento", filename: str):
    tipo = os.path.splitext(filename)[-1].split('.')[-1]
    store_name = f"{instance.nome}.{tipo}"
    return f"documentos/{instance.turma.container.nome_container}/{store_name}"


class ContainerTurma(models.Model):
    nome_container = models.CharField("Tag do Container", max_length=20, null=False, unique=True)
    porta = models.CharField("Porta do container", max_length=6, null=True, unique=True)
    ansible_log = models.TextField("Log do Ansible", null=True)
    ativo = models.BooleanField("Ativo", default=False)

class Turma(models.Model):
    nome_curso = models.CharField("Nome do curso", max_length=200, null=False)
    nome_turma = models.CharField("Nome da turma", max_length=200, null=False)
    container = models.ForeignKey(ContainerTurma, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.nome_curso} - {self.nome_turma}"

class Aluno(models.Model):
    nome = models.CharField("Nome do Aluno", max_length=200, null=False)
    senha = models.CharField("Senha do Aluno", max_length=200, null=False)
    turma =  models.ForeignKey(Turma, on_delete=models.CASCADE, null=True)

class Documento(models.Model):
    nome = models.CharField("Nome do documento", max_length=100, null=False)
    documento = models.FileField(upload_to=upload_documento)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=False)

class UltimaPorta(models.Model):
    ultima_porta: models.CharField = models.CharField("Ultima porta", max_length=6, null=False)