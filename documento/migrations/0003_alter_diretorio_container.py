# Generated by Django 5.1 on 2024-08-16 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documento', '0002_diretorio'),
        ('turmas', '0012_alter_turma_container'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diretorio',
            name='container',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='turmas.containerturma'),
        ),
    ]
