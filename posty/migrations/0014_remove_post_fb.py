# Generated by Django 3.1.3 on 2020-11-27 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0013_post_fb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='fb',
        ),
    ]
