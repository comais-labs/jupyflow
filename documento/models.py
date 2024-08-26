import os
from django.db import models

from ansible.manager import AnsibleManager
from base.settings import BASE_DIR
from documento.utils import upload_file_to_server
from turmas.models import Aluno, ContainerTurma, Turma


def upload_documento(instance: "Documento", filename: str):
    tipo = os.path.splitext(filename)[-1].split(".")[-1]
    store_name = f"{instance.nome}.{tipo}"
    return f"materiais/{store_name}"


class Diretorio(models.Model):
    nome = models.CharField("Nome do diretório", max_length=50, null=False)
    pai = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    container = models.OneToOneField(
        ContainerTurma, on_delete=models.CASCADE, null=True
    )


class DocumentoManager(models.Manager):
    def create_in_container(self, turma: Turma, documento: "Documento"):
        documento.turma = turma

        path_documento = f"{str(BASE_DIR)}/{documento.name}"
        nome_documento = path_documento.split("/")[-1]
        alunos_nome = [
            str(aluno)
            for aluno in Aluno.objects.filter(turma=turma).values_list(
                "nome", flat=True
            )
        ]
        nome_container = turma.container.nome_container
        upload_file_to_server(file_path=path_documento, document_name=nome_documento)

        ansible_manager = AnsibleManager()
        ansible_manager.upload_file_container(
            nome_container=nome_container,
            nome_documento=nome_documento,
            alunos=alunos_nome,
            path_documento=path_documento,
        )
        documento.save()


class Documento(models.Model):
    nome = models.CharField("Nome do documento", max_length=100, null=False)
    documento = models.FileField(upload_to=upload_documento)

    objects = DocumentoManager()
