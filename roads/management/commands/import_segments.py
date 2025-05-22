import csv

from django.core.management.base import BaseCommand
from datetime import datetime

from roads.models import RoadSegment, SpeedReading


class Command(BaseCommand):
    help = "Import road segments and their speed readings from CSV"

    def handle(self, *args, **kwargs):
        path = "data/traffic_speed.csv" 

        created_segments = 0
        created_readings = 0

        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    lat_start = float(row['Lat_start'])
                    long_start = float(row['Long_start'])
                    lat_end = float(row['Lat_end'])
                    long_end = float(row['Long_end'])
                    length = float(row['Length'])
                    speed = float(row['Speed'])
                except Exception as e:
                    self.stderr.write(f"Skipping row due to parsing error: {e}")
                    continue
                
                # Duplicated road segments are ignored
                segment, created = RoadSegment.objects.get_or_create(
                    lat_start=lat_start,
                    long_start=long_start,
                    lat_end=lat_end,
                    long_end=long_end,
                    defaults={'length': length}
                )
                if created:
                    created_segments += 1

                # Add speed reading
                SpeedReading.objects.create(
                    road_segment=segment,
                    speed=speed
                )
                created_readings += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import completed: {created_segments} new segments, {created_readings} readings."
        ))
