# Generated by Django 3.1.3 on 2020-12-26 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201225_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='img/default_avatar.jpg', upload_to='avatar/%y/%m/%d'),
        ),
    ]
