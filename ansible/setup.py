import ansible_runner

from base.settings import BASE_DIR
from turmas.models import ContainerTurma

class ContainerSetup:
    def __init__(self, container: ContainerTurma, alunos: dict):
        self.container = container
        self.alunos = alunos

    def _set_usuarios(self):
        usuarios = []

        for aluno in self.alunos:
            usuarios.append({"user": aluno, "password": aluno})

        self.alunos = usuarios

    def setup(self):
        self._set_usuarios()
        extra_vars = {
            "port_external": 8005,
            "tag_container": self.container.nome_container,
            "users": self.alunos
        }

        runner = ansible_runner.run(
            playbook=f"{BASE_DIR}/ansible/playbook.yml", 
            extravars=extra_vars
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

