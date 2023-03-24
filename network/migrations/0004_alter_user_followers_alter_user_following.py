# Generated by Django 4.1.7 on 2023-03-17 19:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_user_followers_user_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='user_following', to=settings.AUTH_USER_MODEL),
        ),
    ]