# Generated by Django 3.1.3 on 2020-12-22 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0055_auto_20201218_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='fb',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ig',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tt',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]
