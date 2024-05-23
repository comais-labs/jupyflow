from django.db import models

# Create your models here.

class ContainerTurma(models.Model):
    nome_container = models.CharField("Tag do Container", max_length=20, null=False, unique=True)
    ansible_log = models.TextField("Log do Ansible", null=True)
    ativo = models.BooleanField("Ativo", default=False)

class Turma(models.Model):
    nome_curso = models.CharField("Nome do curso", max_length=200, null=False)
    nome_turma = models.CharField("Nome da Turma", max_length=200, null=False)
    alunos = models.JSONField("Lista de alunos", default=None, null=True)
    container = models.ForeignKey(ContainerTurma, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.nome_curso} - {self.nome_turma}"
    
    
