# Generated by Django 5.1.1 on 2024-12-14 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docu_rest_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_uid', models.IntegerField()),
                ('data', models.BinaryField()),
            ],
        ),
    ]