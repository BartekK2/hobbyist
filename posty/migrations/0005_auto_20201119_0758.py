# Generated by Django 3.1.3 on 2020-11-19 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0004_auto_20201119_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='opis',
            field=models.CharField(blank=True, default='Blad! Opis pusty lub nie wczytany', max_length=240, null=True),
        ),
    ]
