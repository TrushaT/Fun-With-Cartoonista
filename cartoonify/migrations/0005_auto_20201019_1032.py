# Generated by Django 2.2 on 2020-10-19 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoonify', '0004_auto_20201016_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='cartoonified_image',
            field=models.ImageField(upload_to='cartoonified_image'),
        ),
    ]
