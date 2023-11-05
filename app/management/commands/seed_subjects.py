from django.core.management.base import BaseCommand
from app.models import Subject
import csv


class Command(BaseCommand):
    help = 'Load data from CSV file'

    def handle(self, *args, **kwargs):
        with open('app/data/subjects.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                obj = Subject()
                obj.title = row[0]
                obj.title_en = row[1]
                obj.save()

