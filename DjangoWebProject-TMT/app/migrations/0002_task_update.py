# Generated by Django 4.2.8 on 2023-12-31 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
