# Generated by Django 5.1.1 on 2024-12-23 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edu_rest_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='task_due_date',
            new_name='assignment_due_date',
        ),
    ]
