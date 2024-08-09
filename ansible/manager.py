import ansible_runner
from django.forms import model_to_dict

from base.settings import BASE_DIR
from turmas.models import ContainerTurma, Turma


class AnsibleManager:
    def __init__(self, container: ContainerTurma = None):
        self.container = container

    def _ansible_run(self, nome_playbook: str, extra_vars: dict):
        runner = ansible_runner.run(
            playbook=f"{BASE_DIR}/ansible/playbooks/{nome_playbook}.yml",
            extravars=extra_vars,
        )

        if runner.status == "failed":
            raise Exception(f"{runner.status}: Não foi possível executar playbook.")

    def _get_models_dict(self, turmas):
        turmas_dict = []
        for turma in turmas:
            if turma:
                turma = model_to_dict(turma)
                container = ContainerTurma.objects.filter(turma=turma["id"]).first()
                if container:
                    turma["porta"] = model_to_dict(container)["porta"]
                    turma["nome_container"] = model_to_dict(container)["nome_container"]
                    turmas_dict.append(turma)
        return turmas_dict

    def _get_usuarios(self, alunos: list | dict):
        if type(alunos) == dict:
            return alunos

        usuarios = []
        for aluno in alunos:
            aluno = {"user": aluno, "password": aluno}
            if aluno not in usuarios:
                usuarios.append(aluno)
        return usuarios

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
            if event_data := teste.get("event_data"):
                if event_data.get("task") == "debug":
                    if res := event_data.get("res"):
                        if res := res.get("results"):
                            for item in res:
                                    item = item.get("msg")
                                    if item.get("stderr_lines"):
                                        resultados.append(
                                            {
                                                "nome_container": item.get("cmd")[-1],
                                                "erro": item.get("stderr"),
                                            }
                                        )
                                    else:
                                        resultados.append(
                                            {
                                                "nome_container": item.get("cmd")[-1],
                                                "estado": item.get("stdout_lines")[0],
                                            }
                                        )
        return resultados

    def run_container(self):
        extra_vars = {"nome_container": self.container.nome_container}
        self._ansible_run(nome_playbook="container_playbook", extra_vars=extra_vars)

    def delete_container(self, nome_container):
        extra_vars = {"nome_container": nome_container}
        self._ansible_run(
            nome_playbook="delete_container_playbook", extra_vars=extra_vars
        )

    def upload_file_container(
        self, nome_container, path_documento, nome_documento, alunos
    ):
        extra_vars = {
            "nome_container": nome_container,
            "path_documento": path_documento,
            "nome_documento": nome_documento,
            "users": alunos,
        }
        self._ansible_run(nome_playbook="upload_file_playbook", extra_vars=extra_vars)

    def setup_container(self, alunos: list, turmas: list):
        extra_vars = {
            "port_external": self.container.porta,
            "tag_container": self.container.nome_container,
            "users": self._get_usuarios(alunos),
            "turmas": self._get_models_dict(turmas),
        }

        self._ansible_run(nome_playbook="playbook", extra_vars=extra_vars)
