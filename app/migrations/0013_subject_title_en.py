# Generated by Django 4.2.2 on 2023-11-03 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_delete_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='title_en',
            field=models.CharField(default='', max_length=100),
        ),
    ]