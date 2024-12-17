import csv
import re
from datetime import datetime

from django.core.management.base import BaseCommand

from restaurant_app.constants.restaurants import DAYS_MAPPING
from restaurant_app.restaurant.models import OperatingHours
from restaurant_app.restaurant.models import Restaurant


class Command(BaseCommand):
    help = "Load restaurant data and operating hours from CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="CSV file with restaurant data",
            required=True,
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs.get("file")

        with open(file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                restaurant, _ = Restaurant.objects.get_or_create(
                    name=row["Restaurant Name"],
                )
                self.parse_and_save_hours(restaurant, row["Hours"])

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully loaded restaurant data and operating hours.",
            ),
        )

    @staticmethod
    def get_time(time_str) -> datetime.time:
        """
        Converts a time string to a datetime.time object.

        Tries to parse the time string in either a 12-hour format without minutes
        (e.g., '3 PM') or with minutes (e.g., '3:30 PM').

        :param time_str: A string representing the time (e.g., '3 PM' or '3:30 PM').
        :return: A datetime.time object representing the parsed time.
        :raises ValueError: If the string does not match either of the expected formats.
        """
        try:
            return datetime.strptime(time_str.strip(), "%I %p").time()
        except ValueError:
            return datetime.strptime(time_str.strip(), "%I:%M %p").time()

    def get_day_range_and_times_from_str(
        self,
        day_time_range: str,
    ) -> tuple[datetime.time, datetime.time, str]:
        """
        Splits a string containing day ranges and time ranges, and parses the time values.

        This function splits the input string into two parts: the day range(s) and the time range(s).
        It then parses the start and end times, returning them as `datetime.time` objects, along with
        the day range(s).

        :param day_time_range: A string containing both the day and time,
                               e.g., "Mon-Fri 11:30 am - 9:30 pm".
        :return: A tuple containing:
                 - start time as a `datetime.time` object
                 - end time as a `datetime.time` object
                 - a string with the day range(s) (e.g., "Mon-Fri, Sun").
        """
        first_digit = re.search(r"\d", day_time_range)
        split_index = first_digit.start()
        day_ranges = day_time_range[:split_index].strip()
        time_range = day_time_range[split_index:].strip()
        start_time_str, end_time_str = time_range.split(" - ")

        start_time = self.get_time(start_time_str)
        end_time = self.get_time(end_time_str)
        return start_time, end_time, day_ranges

    def parse_and_save_hours(self, restaurant: Restaurant, hours_str: str):
        """
        Parses a string of operating hours and saves the parsed hours to the database.

        The function splits the operating hours string into day-time ranges, and for each range,
        it determines the start and end times. It then processes the day ranges (e.g., 'Mon-Fri' or 'Sun')
        and creates the corresponding `OperatingHours` objects for each day.

        :param restaurant: The restaurant object to associate with the operating hours.
        :param hours_str: A string containing the operating hours, e.g.,
        """
        day_time_ranges = hours_str.split("/")
        for day_time_range in day_time_ranges:
            open_time, close_time, day_ranges = self.get_day_range_and_times_from_str(
                day_time_range,
            )
            for day_range in day_ranges.replace(" ", "").split(","):
                if "-" in day_range:
                    start_day, end_day = day_range.split("-")
                    start_day, end_day = start_day.strip(), end_day.strip()
                    start_idx, end_idx = DAYS_MAPPING[start_day], DAYS_MAPPING[end_day]
                    while start_idx <= end_idx:
                        self.get_or_create_operating_hours(
                            restaurant,
                            start_idx,
                            open_time,
                            close_time,
                        )
                        start_idx += 1
                else:
                    day_idx = DAYS_MAPPING[day_range]
                    self.get_or_create_operating_hours(
                        restaurant,
                        day_idx,
                        open_time,
                        close_time,
                    )

    @staticmethod
    def get_or_create_operating_hours(
        restaurant: Restaurant,
        day: int,
        open_time: datetime.time,
        close_time: datetime.time,
    ) -> OperatingHours:
        """
        Retrieves or creates an `OperatingHours` entry for the specified restaurant and day.

        This function gets or creates an`OperatingHours` object.

        :param restaurant: The restaurant object to associate with the operating hours.
        :param day: The day of the week for which the operating hours are  set.
        :param open_time: The time when the restaurant opens.
        :param close_time: The time when the restaurant closes.
        """
        operating_hour, _ = OperatingHours.objects.get_or_create(
            restaurant=restaurant,
            day_of_week=day,
            open_time=open_time,
            close_time=close_time,
        )
        return operating_hour
