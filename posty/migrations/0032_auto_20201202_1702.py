# Generated by Django 3.1.3 on 2020-12-02 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posty', '0031_auto_20201201_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
