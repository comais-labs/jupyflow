# Generated by Django 5.1 on 2024-08-16 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documento', '0003_alter_diretorio_container'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='diretorio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='documento.diretorio'),
        ),
    ]
