# Generated by Django 2.1.4 on 2019-02-10 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_auto_20190210_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='subject',
        ),
    ]