# Generated by Django 3.1.3 on 2020-12-13 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0044_auto_20201213_0311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='city',
        ),
    ]
