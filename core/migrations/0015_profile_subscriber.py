# Generated by Django 4.2.3 on 2023-08-14 08:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0014_alter_post_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscriber',
            field=models.ManyToManyField(related_name='subscribed_user', to=settings.AUTH_USER_MODEL),
        ),
    ]