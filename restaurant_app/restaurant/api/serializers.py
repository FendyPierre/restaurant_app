from mypy.binder import defaultdict
from rest_framework import serializers

from restaurant_app.restaurant.models import OperatingHours
from restaurant_app.restaurant.models import Restaurant


class OperatingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingHours
        fields = ["open_time", "close_time"]


class RestaurantSerializer(serializers.ModelSerializer):
    operating_hours = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ["id", "name", "operating_hours"]

    def get_operating_hours(self, obj):
        hours = defaultdict(list)
        for operating_hours in obj.operating_hours.all():
            hours[operating_hours.get_day_of_week_display()].append(
                [
                    operating_hours.open_time.strftime("%I:%M %p"),
                    operating_hours.close_time.strftime("%I:%M %p"),
                ],
            )
        return hours
