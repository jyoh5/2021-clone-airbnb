from django.db import models
from core import models as core_models


# Create your models here.
class Review(core_models.TimeStampedModel):

    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="reviews"
    )

    # 연결된 object에서 값을 얻을 수 있음
    def __str__(self):
        return f"{self.review} - {self.room}"
        # return self.room.host.username

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6

        return round(avg, 2)

    rating_average.short_description = "avg."
