# Generated by Django 5.1.7 on 2025-03-25 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docu_rest_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersession',
            name='max_docs',
        ),
        migrations.RemoveField(
            model_name='usersession',
            name='max_docs_size',
        ),
    ]
