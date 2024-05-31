import ansible_runner
from django.forms import model_to_dict

from base.settings import BASE_DIR
from turmas.models import ContainerTurma, Turma

class ContainerSetup:
    def __init__(self, container: ContainerTurma, turmas: Turma, alunos: list):
        self.container = container
        self.turmas = turmas
        self.alunos = alunos

    def _set_usuarios(self):
        usuarios = []

        for aluno in self.alunos:
            usuarios.append({"user": aluno, "password": aluno})

        self.alunos = usuarios

    def _get_models_dict(self):
        turmas = []
        for turma in self.turmas:
            turma = model_to_dict(turma)
            turma['porta'] = model_to_dict(ContainerTurma.objects.filter(turma=turma['id']).first())['porta']
            turmas.append(turma)

        return turmas

    def setup(self):
        self._set_usuarios()
        extra_vars = {
            "port_external": self.container.porta,
            "tag_container": self.container.nome_container,
            "users": self.alunos,
            "turmas": self._get_models_dict(),
        }

        breakpoint()

        runner = ansible_runner.run(
            playbook=f"{BASE_DIR}/ansible/playbook.yml", 
            extravars=extra_vars,
        )

        if runner.status == 'failed':
            with runner.stdout as output:
                log = ""
                lines = output.readlines()
                for line in lines:
                    log += f"{line}\n\n"

                self.container.ansible_log = log
                self.container.ativo = False
                self.container.save()
            raise Exception(f"{runner.status}: Não foi possível subir o container da turma.")
        else:
            self.container.ativo = True
            self.container.save()

