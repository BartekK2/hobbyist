# Generated by Django 3.1.3 on 2020-11-28 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0016_auto_20201128_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(default='C:\\Users\\ASUS\\Desktop\\bk_django\\projekt\\src\\meet_me\\static/img/logo.png', upload_to=''),
        ),
    ]