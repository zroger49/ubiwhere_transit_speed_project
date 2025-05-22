import base64
from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models.deletion import ProtectedError
from rest_framework.test import APIClient
from rest_framework import status
from roads.models import RoadSegment, SpeedReading

class RoadSegmentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="", password="admin"
        )

        credentials = base64.b64encode(b"admin:admin").decode("utf-8")
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")

        #self.client.login(username="admin", password="admin")

        self.segment = RoadSegment.objects.create(
            long_start=0.0,
            lat_start=0.0,
            long_end=1.0,
            lat_end=1.0,
            length=100,
            name="segment-one"
        )

        SpeedReading.objects.create(road_segment=self.segment, speed=45.0)

        self.segment2 = RoadSegment.objects.create(
            long_start=0.0,
            lat_start=0.0,
            long_end=1.0,
            lat_end=1.0,
            length=100,
            name="segment-two"
        )


    def test_get_all_roadsegments(self):
        response = self.client.get("/api/roadsegments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "segment-one")

    def test_create_roadsegment(self):
        response = self.client.post("/api/roadsegments/", {
            "long_start": 2.0,
            "lat_start": 2.0,
            "long_end": 3.0,
            "lat_end": 3.0,
            "length": 150,
            "name": "segment-new"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_roadsegment(self):
        segment = RoadSegment.objects.get(name="segment-one")
        response = self.client.patch(f"/api/roadsegments/{segment.id}/", {
            "long_start": 1.0
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["long_start"], 1.0)

    def test_delete_roadsegment_with_readings(self):
        segment = RoadSegment.objects.get(name="segment-one")
        with self.assertRaises(ProtectedError):
            self.client.delete(f"/api/roadsegments/{segment.id}/")
        self.assertTrue(RoadSegment.objects.filter(id=segment.id).exists())
        
    def test_delete_new_roadsegment_without_readings(self):
        segment = RoadSegment.objects.get(name="segment-two")
        response = self.client.delete(f"/api/roadsegments/{self.segment2.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RoadSegment.objects.filter(id=segment.id).exists())
