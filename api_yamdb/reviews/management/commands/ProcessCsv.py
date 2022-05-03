import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from reviews.models import Title

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('D:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\titles.csv', 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                print(row)
                Title.objects.create(id=int(row[0]), name=row[1], year=row[2], category=row[3])