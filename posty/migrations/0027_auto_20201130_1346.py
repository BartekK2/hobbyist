# Generated by Django 3.1.3 on 2020-11-30 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0026_auto_20201130_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='fb',
            field=models.URLField(blank=True, max_length=100),
        ),
    ]
