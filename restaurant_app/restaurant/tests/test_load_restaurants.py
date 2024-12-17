import os
from datetime import time

from django.conf import settings
from django.test import TestCase

from restaurant_app.restaurant.management.commands.load_restaurants import Command
from restaurant_app.restaurant.models import Restaurant


class CommandTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.csv_data = """
        Restaurant Name,Hours
        Test Restaurant,Mon-Fri 11:30 am - 9:30 pm / Sat-Sun 12:00 pm - 10:00 pm
        Another Restaurant,Mon-Sun 10:00 am - 8:00 pm
        """
        cls.csv_file = os.path.join(settings.BASE_DIR, "test_restaurants.csv")
        with open(cls.csv_file, "w") as f:
            f.write(cls.csv_data)

    # def test_command_loads_restaurant_data(self):
    #     call_command('load_restaurants', '--file', self.csv_file)
    #
    #     assert Restaurant.objects.count(), 2)
    #
    #     restaurant1 = Restaurant.objects.get(id=1)
    #     restaurant2 = Restaurant.objects.get(id=2)
    #
    #     assert restaurant1.name, "Test Restaurant")
    #     assert restaurant2.name, "Another Restaurant")

    # def test_command_creates_operating_hours(self):
    #
    #     mock_file = mock.mock_open(read_data=self.csv_data)
    #     mock.mock_open.return_value = mock_file
    #     call_command('load_restaurants', '--file', self.csv_file)
    #
    #     # Verify that the correct number of OperatingHours are created
    #     assert OperatingHours.objects.count(), 4)
    #
    #     # Check if the hours are parsed correctly for Test Restaurant
    #     restaurant = Restaurant.objects.get(name="Test Restaurant")
    #     operating_hours = OperatingHours.objects.filter(restaurant=restaurant).order_by('day_of_week')
    #
    #     # Check if days and times are correct
    #     assert operating_hours[0].day_of_week, DAYS_MAPPING['Mon'])
    #     assert operating_hours[0].open_time, time(11, 30))
    #     assert operating_hours[0].close_time, time(21, 30))
    #
    #     assert operating_hours[3].day_of_week, DAYS_MAPPING['Sun'])
    #     assert operating_hours[3].open_time, time(12, 00))
    #     assert operating_hours[3].close_time, time(22, 00))

    def test_parse_and_save_hours_valid(self):
        restaurant = Restaurant.objects.create(name="Test Restaurant")
        hours_str = "Mon-Fri 11:30 am - 9:30 pm / Sat-Sun 12:00 pm - 10:00 pm"

        command = Command()
        command.parse_and_save_hours(restaurant, hours_str)

        operating_hours = restaurant.operating_hours
        assert operating_hours.count() == 7

    def test_parse_and_save_hours_invalid(self):
        restaurant = Restaurant.objects.create(name="Test Restaurant")
        invalid_hours_str = "Mon-Sun 10:00 am - 8:00 pm / InvalidDay 10:00 am - 8:00 pm"

        command = Command()
        assert restaurant.operating_hours.count() == 0
        with self.assertRaises(KeyError):
            command.parse_and_save_hours(restaurant, invalid_hours_str)

        assert restaurant.operating_hours.count() == 7

    def test_get_time_method(self):
        time1 = Command.get_time("3 PM")
        time2 = Command.get_time("3:30 PM")

        assert time1 == time(15, 0)
        assert time2 == time(15, 30)

        with self.assertRaises(ValueError):
            Command.get_time("invalid time")

    # def test_handle_method(self):
    #     mock_csv = StringIO(self.csv_data)
    #     call_command('load_restaurants', '--file', mock_csv)
    #
    #     assert Restaurant.objects.count(), 2)
    #     assert OperatingHours.objects.count(), 4)
    #
    #     restaurant = Restaurant.objects.get(name="Test Restaurant")
    #     operating_hours = OperatingHours.objects.filter(restaurant=restaurant)
    #
    #     assert operating_hours[0].day_of_week, DAYS_MAPPING['Mon'])
    #     assert operating_hours[0].open_time, time(11, 30))
    #     assert operating_hours[0].close_time, time(21, 30))

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.csv_file)
