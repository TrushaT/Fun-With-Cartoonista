# Generated by Django 2.2 on 2020-10-20 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_auto_20201020_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header_image',
            field=models.ImageField(upload_to='posts'),
        ),
    ]
