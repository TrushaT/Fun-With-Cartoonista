# Generated by Django 2.2 on 2020-10-15 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20200905_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header_image',
            field=models.ImageField(upload_to='post_images'),
        ),
    ]