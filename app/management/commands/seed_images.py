from django.core.management.base import BaseCommand
from app.models import Image, Artist, AI, Subject
import csv
import os
from django.core.files import File


class Command(BaseCommand):
    help = 'Load data from CSV file'

    def handle(self, *args, **kwargs):
        with open('app/data/images.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                obj = Image()
                try:
                    name, last_name = row[1].split()
                except ValueError:
                    name, temp1, temp2 = row[1].split()
                    last_name = temp1+' '+temp2
                obj.style = Artist.objects.get(first_name=name, last_name=last_name)
                obj.ai = AI.objects.get(name="Stable Diffusion")
                obj.subject = Subject.objects.get(title_en=row[0])
                with open(os.path.join('app/data/images', row[2]), 'rb') as img:
                    obj.photo.save(row[2], File(img))
                obj.save()
