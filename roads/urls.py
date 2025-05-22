from django.urls import path, include
from rest_framework import routers
from .views import RoadSegmentViewSet, SpeedReadingViewSet, bulk_car_passage_upload, get_passages_by_license_plate

router = routers.DefaultRouter()
router.register(r'roadsegments', RoadSegmentViewSet)
router.register(r'speedreadings', SpeedReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('car_passages/bulk/', bulk_car_passage_upload, name='bulk_passage_upload'),
    path('car_passages/', get_passages_by_license_plate, name='get_passages_by_license_plate'),
]
