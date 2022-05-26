# Generated by Django 3.2.8 on 2022-05-18 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoApp', '0002_category_subscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='video',
            field=models.ManyToManyField(through='videoApp.VideoCategory', to='videoApp.Video'),
        ),
    ]
