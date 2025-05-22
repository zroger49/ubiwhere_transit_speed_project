from django.db.models import OuterRef, Subquery,Case, When, Value, FloatField, CharField
from django.utils.timezone import now, timedelta

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .consts import HIGH_TRAFIC_SPEED, MEDIUM_TRAFIC_SPEED 
from .models import RoadSegment, SpeedReading, CarPassage, Cars
from .serializers import RoadSegmentSerializer, SpeedReadingSerializer, CarPassageSerializer
from .permissions import IsAdmin

import os

SENSOR_API_KEY = os.getenv('SENSOR_API_KEY')


class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=['get'])
    def speedreading_count(self, request, pk=None):
        try:
            segment = self.get_object()
            count = segment.speed_readings.count()
            return Response({"road_segment_id": segment.id, "speed_reading_count": count})
        except RoadSegment.DoesNotExist:
            return Response({"error": "Road segment not found."}, status=404)
        
    def get_queryset(self):
        queryset = super().get_queryset()

        transit_speed = self.request.query_params.get('transit_speed')
        if transit_speed in ['high', 'medium', 'low']:
            subquery = SpeedReading.objects.filter(
                road_segment=OuterRef('pk')
            ).order_by('-timestamp')

            queryset = queryset.annotate(
                latest_speed=Subquery(subquery.values('speed')[:1],
                                       output_field=FloatField())
            ).annotate(
                latest_intensity=Case(
                    When(latest_speed__lte=HIGH_TRAFIC_SPEED, then=Value('high')),
                    When(latest_speed__lte=MEDIUM_TRAFIC_SPEED, then=Value('medium')),
                    default=Value('low'),
                    output_field=CharField(),
                ) # Added this annotation to classify the speed, since I was having trouble acessing the "INTENSITY" field
            ).filter(latest_intensity=transit_speed)

        return queryset

class SpeedReadingViewSet(viewsets.ModelViewSet):
    queryset = SpeedReading.objects.all()
    serializer_class = SpeedReadingSerializer
    permission_classes = [IsAdmin]


# Since there is not need for the View in the admin pannel, create a funcion based view instead a class based view
@api_view(['POST'])
@permission_classes([AllowAny])
def bulk_car_passage_upload(request):
    if request.headers.get('X-API-KEY') != SENSOR_API_KEY:
        return Response({'error': 'Invalid or missing API key'}, status=status.HTTP_403_FORBIDDEN)

    serializer = CarPassageSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdmin])
def get_passages_by_license_plate(request):
    license_plate = request.query_params.get('license_plate')
    if not license_plate:
        return Response({'error': 'license_plate parameter is required'}, status=400)

    try:
        car = Cars.objects.get(license_plate=license_plate)
    except Cars.DoesNotExist:
        return Response({'error': 'Car not found'}, status=404)

    #since = now() - timedelta(hours=24)
    #timestamp__gte=since
    passages = CarPassage.objects.filter(car=car).select_related('sensor', 'road_segment','car')

    data = [{
        'timestamp': p.timestamp,
        'sensor': {'uuid': p.sensor.uuid, 'name': p.sensor.name},
        'road_segment': {
            'id': p.road_segment.id,
            'name': p.road_segment.name,
            'coordinates': {
                'start': [p.road_segment.lat_start, p.road_segment.long_start],
                'end': [p.road_segment.lat_end, p.road_segment.long_end],
            }
        }, 
        "car": {
            'license_plate': p.car.license_plate,
            'created_at': p.car.created_at
        },
    } for p in passages]

    return Response(data, status=200)