# Generated by Django 4.2.2 on 2023-09-24 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_artist_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='photo',
            field=models.ImageField(default='', upload_to='mediafiles/artists'),
        ),
    ]