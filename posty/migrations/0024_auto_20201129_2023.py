# Generated by Django 3.1.3 on 2020-11-29 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0023_auto_20201129_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ig',
            field=models.URLField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tt',
            field=models.URLField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='fb',
            field=models.URLField(blank=True, max_length=100),
        ),
    ]