# Generated by Django 5.0.6 on 2024-05-30 00:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turmas', '0007_alter_aluno_senha'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='turma',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='turmas.turma'),
        ),
    ]
