from django.core.management.base import BaseCommand
from app.models import Artist
import csv
import os
from django.core.files import File


class Command(BaseCommand):
    help = 'Load data from CSV file'

    def handle(self, *args, **kwargs):
        with open('app/data/artists.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                obj = Artist()
                obj.first_name = row[0]
                obj.last_name = row[1]
                obj.description = row[2]
                with open(os.path.join('app/data/artists_images', row[3]), 'rb') as img:
                    obj.photo.save(row[3], File(img))
                obj.save()

