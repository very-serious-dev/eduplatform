# Generated by Django 5.1.7 on 2025-07-05 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edu_app', '0015_alter_post_assignment_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='is_autogenerated',
        ),
    ]
