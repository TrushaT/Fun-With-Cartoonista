# Generated by Django 2.2 on 2020-10-16 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cartoonified_image', models.ImageField(upload_to='cartoonified_image')),
                ('original_image', models.ImageField(upload_to='original_image')),
            ],
        ),
    ]