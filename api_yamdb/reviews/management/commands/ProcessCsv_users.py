import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('D:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\users.csv', 'r', encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                print(row)
                User.objects.create(id=int(row[0]), username=row[1], email=row[2], role=row[3])