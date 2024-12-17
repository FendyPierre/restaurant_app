from django.contrib import admin

from .models import OperatingHours
from .models import Restaurant


class OperatingHoursInline(admin.TabularInline):
    model = OperatingHours
    extra = 1
    fields = ["day_of_week", "open_time", "close_time"]
    ordering = ["day_of_week"]


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [OperatingHoursInline]
