from django.core.management.base import BaseCommand
from app.models import AI
import csv


class Command(BaseCommand):
    help = 'Load data from CSV file'

    def handle(self, *args, **kwargs):
        with open('app/data/ai.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                obj = AI()
                obj.name = row[0]
                obj.creator = row[1]
                obj.link = row[2]
                obj.save()

