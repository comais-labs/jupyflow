# Generated by Django 5.0.6 on 2024-05-16 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turmas', '0003_containerturma_remove_turma_tag_turma_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='containerturma',
            name='ansible_log',
            field=models.TextField(null=True, verbose_name='Log do Ansible'),
        ),
    ]
