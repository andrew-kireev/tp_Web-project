# Generated by Django 3.1.3 on 2020-12-25 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201225_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default_avatar.jpg', null=True, upload_to='avatar/%y/%m/%d'),
        ),
    ]
