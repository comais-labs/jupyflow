import ansible_runner
from django.forms import model_to_dict

from base.settings import BASE_DIR
from turmas.models import ContainerTurma, Turma


class AnsibleManager:
    def __init__(self, container: ContainerTurma):
        self.container = container

    def _ansible_run(self, nome_playbook: str, extra_vars: dict):
        runner = ansible_runner.run(
            playbook=f"{BASE_DIR}/ansible/playbooks/{nome_playbook}.yml",
            extravars=extra_vars,
            ident="health_check",
        )
        resultados = []
        for teste in runner.events:
            if teste['event_data'].get('task') == 'debug':
                if res := teste['event_data'].get('res'):
                    if res := res.get('results'):
                        for item in res:
                            item = item.get('msg')
                            resultados.append({
                                "nome_container": item.get('cmd')[-1],
                                "estado": item.get('stdout_lines')[0]
                            })
        print(resultados)

        if runner.status == "failed":
            with runner.stdout as output:
                log = ""
                lines = output.readlines()
                for line in lines:
                    log += line
                self.container.ansible_log = log
                self.container.ativo = False
                self.container.save()
            raise Exception(
                f"{runner.status}: Não foi possível subir o container da turma."
            )
        else:
            ...
            # self.container.ativo = True
            # self.container.save()

    def _get_models_dict(self, turmas):
        turmas_dict = []
        for turma in turmas:
            turma = model_to_dict(turma)
            turma["porta"] = model_to_dict(
                ContainerTurma.objects.filter(turma=turma["id"]).first()
            )["porta"]
            turmas_dict.append(turma)
        return turmas_dict

    def _get_usuarios(self, alunos: list | dict):
        if type(alunos) == dict:
            return alunos
        return [{"user": aluno, "password": aluno} for aluno in alunos]

    def adicionar_alunos_container(self, alunos: list):
        extra_vars = {
            "nome_container": self.container.nome_container,
            "users": self._get_usuarios(alunos),
        }
        self._ansible_run(nome_playbook="usuario_playbook", extra_vars=extra_vars)

    def healthcheck_containers(self, containers: list[str]):
        extra_vars = {"containers": containers}
        runner = ansible_runner.run(
            playbook=f"{BASE_DIR}/ansible/playbooks/healthcheck_playbook.yml",
            extravars=extra_vars,
        )

        resultados = []
        for teste in runner.events:
            if teste['event_data'].get('task') == 'debug':
                if res := teste['event_data'].get('res'):
                    if res := res.get('results'):
                        for item in res:
                            item = item.get('msg')
                            resultados.append({
                                "nome_container": item.get('cmd')[-1],
                                "estado": item.get('stdout_lines')[0]
                            })

        return resultados

    def run_container(self):
        extra_vars = {"nome_container": self.container.nome_container}
        self._ansible_run(nome_playbook="container_playbook", extra_vars=extra_vars)

    def setup_container(self, alunos: list, turmas: list):
        extra_vars = {
            "port_external": self.container.porta,
            "tag_container": self.container.nome_container,
            "users": self._get_usuarios(alunos),
            "turmas": self._get_models_dict(turmas),
        }

        self._ansible_run(nome_playbook="playbook", extra_vars=extra_vars)
