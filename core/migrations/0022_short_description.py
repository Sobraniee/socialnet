# Generated by Django 4.2.3 on 2023-08-18 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_profile_link_fb_profile_photo_profile_telegram_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='short',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
