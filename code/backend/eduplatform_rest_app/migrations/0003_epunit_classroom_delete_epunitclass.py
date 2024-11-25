# Generated by Django 5.1.1 on 2024-11-25 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduplatform_rest_app', '0002_epunitclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='epunit',
            name='classroom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='eduplatform_rest_app.epclass'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='EPUnitClass',
        ),
    ]
