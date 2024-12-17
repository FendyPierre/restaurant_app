from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant_app.restaurant.api.serializers import RestaurantSerializer
from restaurant_app.restaurant.selectors import RestaurantSelector


class RestaurantByDateTimeAPIView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        datetime_str = request.query_params.get("datetime")
        if not datetime_str:
            return Response(
                {"error": 'Please provide a datetime parameter "datetime"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            query_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return Response(
                {"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        restaurants = RestaurantSelector.get_restaurants_by_datetime(
            query_datetime,
        ).prefetch_related("operating_hours")

        return Response(
            {"open_restaurants": RestaurantSerializer(restaurants, many=True).data},
        )
