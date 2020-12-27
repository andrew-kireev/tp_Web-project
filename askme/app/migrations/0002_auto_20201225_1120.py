# Generated by Django 3.1.3 on 2020-12-25 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='img',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default_avatar.jpg', upload_to='avatar/'),
        ),
    ]
