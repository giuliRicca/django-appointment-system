# Generated by Django 4.0.5 on 2022-11-09 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_service_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='length',
        ),
    ]
