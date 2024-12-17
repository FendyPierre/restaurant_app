import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from restaurant_app.restaurant.models import OperatingHours
from restaurant_app.restaurant.models import Restaurant


class RestaurantByDateTimeAPIViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:restaurant_by_datetime_api_view")
        self.restaurant_1 = Restaurant.objects.create(name="Restaurant 1")
        self.restaurant_2 = Restaurant.objects.create(name="Restaurant 2")

        self.operating_hours_1 = [
            OperatingHours.objects.create(
                restaurant=self.restaurant_1,
                day_of_week=0,
                open_time=datetime.time(11, 0),
                close_time=datetime.time(22, 0),
            ),
            OperatingHours.objects.create(
                restaurant=self.restaurant_1,
                day_of_week=1,
                open_time=datetime.time(11, 0),
                close_time=datetime.time(22, 0),
            ),
            OperatingHours.objects.create(
                restaurant=self.restaurant_1,
                day_of_week=2,
                open_time=datetime.time(11, 0),
                close_time=datetime.time(22, 0),
            ),
        ]

        self.operating_hours_2 = [
            OperatingHours.objects.create(
                restaurant=self.restaurant_2,
                day_of_week=0,
                open_time=datetime.time(9, 0),
                close_time=datetime.time(18, 0),
            ),
            OperatingHours.objects.create(
                restaurant=self.restaurant_2,
                day_of_week=1,
                open_time=datetime.time(9, 0),
                close_time=datetime.time(18, 0),
            ),
        ]

    def test_missing_datetime_parameter(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "error": 'Please provide a datetime parameter "datetime"',
        }

    def test_invalid_datetime_format(self):
        invalid_datetime = "2024-12-16 25:00:00"
        response = self.client.get(self.url, {"datetime": invalid_datetime})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}

    def test_valid_datetime_with_open_restaurants(self):
        valid_datetime = "2024-12-18 12:00:00"
        response = self.client.get(self.url, {"datetime": valid_datetime})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["open_restaurants"]) == 1
        assert response.data["open_restaurants"][0]["name"] == self.restaurant_1.name

    def test_valid_datetime_with_multiple_open_restaurants(self):
        valid_datetime = "2024-12-16 12:00:00"
        response = self.client.get(self.url, {"datetime": valid_datetime})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["open_restaurants"]) == 2
        restaurant_names = [
            restaurant["name"] for restaurant in response.data["open_restaurants"]
        ]
        assert self.restaurant_1.name == restaurant_names
        assert self.restaurant_2.name == restaurant_names

    def test_valid_datetime_with_no_open_restaurants(self):
        valid_datetime = "2024-12-16 23:00:00"
        response = self.client.get(self.url, {"datetime": valid_datetime})
        assert response.status_code == status.HTTP_200_OK
        assert "open_restaurants" in response.data
        assert len(response.data["open_restaurants"]) == 0

    def tearDown(self):
        Restaurant.objects.all().delete()
        OperatingHours.objects.all().delete()
