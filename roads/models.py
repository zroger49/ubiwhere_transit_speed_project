import codename

from django.db import models
from django.utils import timezone

from .consts import HIGH_TRAFIC_SPEED, MEDIUM_TRAFIC_SPEED

class RoadSegment(models.Model):
    #Note: there is probably a dedicated field for geolocation but this is a simple implementation
    long_start = models.FloatField()
    lat_start = models.FloatField()
    long_end = models.FloatField()
    lat_end = models.FloatField()
    length = models.FloatField()

    name = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        help_text="Unique sensor name (e.g., 'noisy-panda')"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lat_start', 'long_start', 'lat_end', 'long_end', 'name'],
                name='unique_roadsegment_coordinates'
            ),
        ]

    def __str__(self):
        return f"Segment {self.id}: ({self.long_start}, {self.lat_start}) to ({self.long_end}, {self.lat_end})"
    

    def save(self, *args, **kwargs):
        if not self.name:
            while True: # This can lead to an infinite loop if all names are taken, but it is unlikely in this application
                candidate = codename.codename(separator = "-")
                if not RoadSegment.objects.filter(name=candidate).exists():
                    self.name = candidate
                    break
        super().save(*args, **kwargs)

    
    @property
    def reading_count(self, methods=['get']):
        return self.speed_readings.count() # This uses the reverse relation from SpeedReading to RoadSegment via related_name='speed_readings'



class SpeedReading(models.Model):
    road_segment = models.ForeignKey(
        RoadSegment,
        on_delete=models.PROTECT,
        related_name='speed_readings'
    )
    speed = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.road_segment.name}"

    @property
    def intensity(self):
        """
        Determine intensity based on speed.
        This must reflect current rules always.
        """
        if self.speed <= HIGH_TRAFIC_SPEED:
            return "elevada"
        elif HIGH_TRAFIC_SPEED < self.speed <= MEDIUM_TRAFIC_SPEED:
            return "média"
        else:
            return "baixa"


class Sensors(models.Model): 
    name = models.CharField(max_length=100, unique=True)
    uuid = models.UUIDField(unique=True)

    def __str__(self):
        return self.name
    
class Cars(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.license_plate

class CarPassage(models.Model):
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.PROTECT)
    car = models.ForeignKey(Cars, on_delete=models.PROTECT)
    sensor = models.ForeignKey(Sensors, on_delete=models.PROTECT)
    timestamp = models.DateTimeField() # No auto_now_add=True because the data gets sent in bulk from the sensors

    def __str__(self):
        return f"{self.car.license_plate} at {self.timestamp}"