from django.db import models


class DayOfWeek(models.IntegerChoices):
    MONDAY = (0, "Monday")
    TUESDAY = (1, "Tuesday")
    WEDNESDAY = (2, "Wednesday")
    THURSDAY = (3, "Thursday")
    FRIDAY = (4, "Friday")
    SATURDAY = (5, "Saturday")
    SUNDAY = (6, "Sunday")


class Restaurant(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class OperatingHours(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name="operating_hours",
        on_delete=models.CASCADE,
    )
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        ordering = ["day_of_week", "open_time", "close_time"]

    def __str__(self):
        day_name = DayOfWeek(self.day_of_week).label
        return (
            f"{day_name}: {self.open_time.strftime('%I:%M %p')} - "
            f"{self.close_time.strftime('%I:%M %p')}"
        )
