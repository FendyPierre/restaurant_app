import datetime

from django.test import TestCase

from restaurant_app.restaurant.models import DayOfWeek
from restaurant_app.restaurant.models import OperatingHours
from restaurant_app.restaurant.models import Restaurant
from restaurant_app.restaurant.selectors import RestaurantSelector


class RestaurantSelectorTests(TestCase):
    def setUp(self):
        self.restaurant_1 = Restaurant.objects.create(name="Restaurant 1")
        self.restaurant_2 = Restaurant.objects.create(name="Restaurant 2")

        self.operating_hours_1 = [
            OperatingHours.objects.create(
                restaurant=self.restaurant_1,
                day_of_week=DayOfWeek.MONDAY,
                open_time=datetime.time(11, 0),
                close_time=datetime.time(22, 0),
            ),
            OperatingHours.objects.create(
                restaurant=self.restaurant_1,
                day_of_week=DayOfWeek.TUESDAY,
                open_time=datetime.time(11, 0),
                close_time=datetime.time(22, 0),
            ),
        ]

        self.operating_hours_2 = [
            OperatingHours.objects.create(
                restaurant=self.restaurant_2,
                day_of_week=DayOfWeek.MONDAY,
                open_time=datetime.time(9, 0),
                close_time=datetime.time(18, 0),
            ),
            OperatingHours.objects.create(
                restaurant=self.restaurant_2,
                day_of_week=DayOfWeek.WEDNESDAY,
                open_time=datetime.time(9, 0),
                close_time=datetime.time(18, 0),
            ),
        ]

    def test_get_restaurants_by_datetime(self):
        test_datetime_1 = datetime.datetime(2024, 12, 16, 12, 0)
        restaurants_1 = RestaurantSelector.get_restaurants_by_datetime(test_datetime_1)
        assert self.restaurant_1 in restaurants_1
        assert self.restaurant_2 in restaurants_1

        test_datetime_2 = datetime.datetime(2024, 12, 17, 10, 0)
        restaurants_2 = RestaurantSelector.get_restaurants_by_datetime(test_datetime_2)
        assert self.restaurant_1 in restaurants_2
        assert self.restaurant_2 in restaurants_2

        test_datetime_4 = datetime.datetime(2024, 12, 18, 10, 0)
        restaurants_4 = RestaurantSelector.get_restaurants_by_datetime(test_datetime_4)
        assert self.restaurant_1 in restaurants_4
        assert self.restaurant_2 in restaurants_4

        test_datetime_3 = datetime.datetime(2024, 12, 19, 10, 0)
        restaurants_3 = RestaurantSelector.get_restaurants_by_datetime(test_datetime_3)
        assert self.restaurant_1 in restaurants_3
        assert self.restaurant_2 in restaurants_3
