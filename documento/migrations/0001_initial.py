# Generated by Django 5.1 on 2024-08-12 15:21

import django.db.models.deletion
import documento.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('turmas', '0011_delete_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do documento')),
                ('documento', models.FileField(upload_to=documento.models.upload_documento)),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turmas.turma')),
            ],
        ),
    ]
