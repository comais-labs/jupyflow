import os
import tempfile
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile

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
    def __get_file_path(self, filename: str):
        return f"/home/comais/documentos/{filename}"

    def _create_in_container(
        self,
        path_documento: str,
        nome_documento: str,
        nomes_alunos: str,
        nome_container: str,
    ):
        upload_file_to_server(file_path=path_documento, document_name=nome_documento)

        ansible_manager = AnsibleManager()
        ansible_manager.upload_file_container(
            nome_container=nome_container,
            nome_documento=nome_documento,
            alunos=nomes_alunos,
            path_documento=path_documento,
        )

    def create_one(self, turma: Turma, documento: "Documento"):
        documento.save()

        path_documento = f"{str(BASE_DIR)}/{documento.documento.name}"
        nome_documento = path_documento.split("/")[-1]
        nome_container = turma.container.nome_container

        nomes_alunos = [
            str(aluno)
            for aluno in Aluno.objects.filter(turma=turma).values_list(
                "nome", flat=True
            )
        ]

        self._create_in_container(
            path_documento=path_documento,
            nome_documento=nome_documento,
            nomes_alunos=nomes_alunos,
            nome_container=nome_container,
        )

    def create_multiple(
        self, nome: str, turmas: list[str], documento: InMemoryUploadedFile
    ):
        turmas = [Turma.objects.filter(id=id).first() for id in turmas]
        extensao = documento.name.split(".")[-1]
        nome_documento = f"{nome}.{extensao}"

        documento.caminho = self.__get_file_path(nome_documento)
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(documento.read())

            for turma in turmas:
                nomes_alunos = [
                    str(aluno)
                    for aluno in Aluno.objects.filter(turma=turma.id).values_list(
                        "nome", flat=True
                    )
                ]

                nome_container = turma.container.nome_container
                self._create_in_container(
                    path_documento=tmp.name,
                    nome_documento=nome_documento,
                    nomes_alunos=nomes_alunos,
                    nome_container=nome_container,
                )


class Documento(models.Model):
    nome = models.CharField("Nome do documento", max_length=100, null=False)
    caminho = models.CharField("Caminho do documento", max_length=256, null=True)

    objects = DocumentoManager()
