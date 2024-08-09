import logging
from typing import Container

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from ansible.manager import AnsibleManager
from turmas.models import ContainerTurma

logger = logging.getLogger(__name__)


def __update_container_state(estados: list[dict]):
    for container in estados:
        ativo = True if container.get("estado") == "running" else False
        container_model = ContainerTurma.objects.filter(
            nome_container=container["nome_container"]
        ).first()
        if container_model.ativo != ativo:
            container_model.ativo = ativo

        if mensagem := container.get("erro"): 
            container_model.mensagem_erro = mensagem
        
        container_model.save()


def healthcheck_containers():
    container_aux = ContainerTurma.objects.first()
    containers = ContainerTurma.objects.all().values_list("nome_container", flat=True)
    nome_containers = []
    for container_name in containers:
        nome_containers.append(str(container_name))

    resultados = AnsibleManager(container=container_aux).healthcheck_containers(
        nome_containers
    )
    if resultados:
        __update_container_state(resultados)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=1):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            healthcheck_containers,
            trigger=CronTrigger(minute="*"),  # Every 10 seconds
            id="healthcheck_containers",  # The `id` assigned to each job MUST be unique
            max_instances=2,
            replace_existing=True,
        )
        logger.info("Added job 'healthcheck'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
