# Generated by Django 3.1.3 on 2021-01-02 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0059_auto_20210102_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='birthday',
        ),
    ]
