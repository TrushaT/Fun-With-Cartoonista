# Generated by Django 2.2 on 2020-10-15 18:30

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20201015_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header_image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/media/post_images'), upload_to=''),
        ),
    ]
