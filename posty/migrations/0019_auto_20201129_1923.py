# Generated by Django 3.1.3 on 2020-11-29 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0018_auto_20201129_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(default=12),
        ),
    ]
