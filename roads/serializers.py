from rest_framework import serializers
from .models import RoadSegment, SpeedReading, CarPassage, Cars, Sensors

class RoadSegmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RoadSegment
        fields = "__all__" #This is fine since because there is no sensitive data, Same for SpeedReadingSerializer


class SpeedReadingSerializer(serializers.ModelSerializer):
    intensity = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SpeedReading
        fields = "__all__"

    def get_intensity(self, obj):
        return obj.intensity


class SensorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensors
        fields = "__all__"
    
class CarsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cars
        fields = "__all__"


class CarPassageSerializer(serializers.ModelSerializer):
    road_segment = serializers.PrimaryKeyRelatedField(queryset=RoadSegment.objects.all())
    car__license_plate = serializers.CharField(write_only=True)
    sensor__uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = CarPassage
        fields = ['road_segment', 'timestamp', 'car__license_plate', 'sensor__uuid']

    def create(self, data):
        license_plate = data.pop('car__license_plate')
        sensor_uuid = data.pop('sensor__uuid')

        car, _ = Cars.objects.get_or_create(license_plate=license_plate)
        try:
            sensor = Sensors.objects.get(uuid=sensor_uuid)
        except Sensors.DoesNotExist:
            raise serializers.ValidationError("Invalid sensor UUID")

        return CarPassage.objects.create(car=car, sensor=sensor, **data)
