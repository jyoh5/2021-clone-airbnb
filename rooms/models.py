# import os # 1 python package
from django.db import models  # 2 django package
from django.urls import reverse
from django_countries.fields import CountryField  # 3 third-party package
from core import models as core_models  # 4 custom package

# from users import models as user_models


# Create your models here.
class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]

    pass


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"

    pass


class Facility(AbstractItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"

    pass


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"

    pass


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="photos")

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rooms"
    )
    room_type = models.ForeignKey(
        RoomType, on_delete=models.SET_NULL, null=True, related_name="rooms"
    )
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="rooms")
    facilities = models.ManyToManyField(Facility, blank=True, related_name="rooms")
    house_rules = models.ManyToManyField(HouseRule, blank=True, related_name="rooms")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})
        # return "/go"
