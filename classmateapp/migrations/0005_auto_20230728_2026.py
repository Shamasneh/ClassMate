# Generated by Django 3.2.20 on 2023-07-28 20:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classmateapp', '0004_room_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='members',
        ),
        migrations.AddField(
            model_name='room',
            name='room_members',
            field=models.ManyToManyField(blank=True, related_name='room_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
