# Generated by Django 2.0.13 on 2019-08-13 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190813_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default.png', upload_to=None),
        ),
    ]
