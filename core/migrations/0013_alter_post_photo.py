# Generated by Django 4.2.3 on 2023-08-14 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_comment_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(null=True, upload_to='photo_post/', verbose_name='Фотография'),
        ),
    ]