# Generated by Django 4.2.2 on 2023-11-15 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_userimagepreferences'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userimagepreferences',
            old_name='number_of_images',
            new_name='steps',
        ),
        migrations.RemoveField(
            model_name='userimagepreferences',
            name='number_of_steps',
        ),
    ]
