# Generated by Django 3.1.3 on 2020-12-08 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0040_auto_20201206_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='place',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
