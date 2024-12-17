from django.urls import path

from restaurant_app.restaurant.api import views

urlpatterns = [
    path(
        "",
        views.RestaurantByDateTimeAPIView.as_view(),
        name="restaurant_by_datetime_api_view",
    ),
]
