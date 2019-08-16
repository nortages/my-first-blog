# Generated by Django 2.0.13 on 2019-08-12 19:44

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190809_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default.png', upload_to=blog.models.path_and_rename),
        ),
    ]