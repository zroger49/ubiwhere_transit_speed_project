import csv
from django.core.management.base import BaseCommand
from roads.models import Sensors

class Command(BaseCommand):
    help = 'Import sensors from CSV'

    def handle(self, *args, **kwargs):
        with open('data/sensors.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Sensors.objects.get_or_create(
                    uuid=row['uuid'],
                    defaults={'name': row['name']}
                )
        self.stdout.write(self.style.SUCCESS('Sensors imported successfully'))
