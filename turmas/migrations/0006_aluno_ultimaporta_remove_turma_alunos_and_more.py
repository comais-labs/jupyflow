# Generated by Django 5.0.6 on 2024-05-29 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turmas', '0005_alter_containerturma_ativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome do Aluno')),
                ('senha', models.CharField(max_length=200, verbose_name='Nome do Aluno')),
            ],
        ),
        migrations.CreateModel(
            name='UltimaPorta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ultima_porta', models.CharField(max_length=6, verbose_name='Ultima porta')),
            ],
        ),
        migrations.RemoveField(
            model_name='turma',
            name='alunos',
        ),
        migrations.AddField(
            model_name='containerturma',
            name='porta',
            field=models.CharField(max_length=6, null=True, unique=True, verbose_name='Porta do container'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='nome_turma',
            field=models.CharField(max_length=200, verbose_name='Nome da turma'),
        ),
    ]
