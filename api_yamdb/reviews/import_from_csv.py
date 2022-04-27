import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from models import Title

class Command(BaseCommand):
    def handle(self, *args, **options):
        with(os.join.path(settings.BASE_DIR / 'api_yamdb/static/data/titles.csv'), 'r') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                Title.objects.create(name=row[2], year=row[3], category=row[4])