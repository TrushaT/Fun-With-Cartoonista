# Generated by Django 2.2 on 2020-10-16 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartoonify', '0003_auto_20201016_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='original_image',
            field=models.ImageField(upload_to='original_image'),
        ),
    ]
