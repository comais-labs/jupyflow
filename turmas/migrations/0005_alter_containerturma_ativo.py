# Generated by Django 5.0.6 on 2024-05-23 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turmas', '0004_containerturma_ansible_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='containerturma',
            name='ativo',
            field=models.BooleanField(default=False, verbose_name='Ativo'),
        ),
    ]
