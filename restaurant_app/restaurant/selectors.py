import datetime

from django.apps import apps
from django.db.models import QuerySet

Restaurant = apps.get_model("restaurant", "Restaurant")


class RestaurantSelector:
    """
    A class responsible for handling restaurant queries.

    Methods:
    ----------
    get_restaurants_by_datetime(dt: datetime.datetime) -> QuerySet[Restaurant]:
        Returns a queryset of restaurants that are open at the provided datetime.
    """

    @staticmethod
    def get_restaurants_by_datetime(dt: datetime.datetime) -> QuerySet[Restaurant]:
        """
        Returns a list of restaurants that are open at the specified datetime.

        :param dt: A `datetime` object representing the date and time to check.
        :return: `Restaurant` Queryset
        """

        return Restaurant.objects.filter(
            operating_hours__day_of_week=dt.weekday(),
            operating_hours__open_time__lte=dt.time(),
            operating_hours__close_time__gte=dt.time(),
        )
