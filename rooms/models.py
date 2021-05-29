from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from core import models as core_models
from cal import Calendar


class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item """

    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """ RoomType Object Definition """

    pass

    class Meta:
        verbose_name = _("Room Type")
        ordering = ["name"]


class Amenity(AbstractItem):
    """ Amenity Object Definition """

    pass

    class Meta:
        verbose_name_plural = _("Amenities")


class Facility(AbstractItem):
    """ Facility Model Definition """

    pass

    class Meta:
        verbose_name_plural = _("Facilities")


class HouseRule(AbstractItem):
    """ HouseRule Model Definition """

    pass

    class Meta:
        verbose_name = _("House Rule")


class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    # file = models.ImageField(upload_to="room_photos")
    file = ProcessedImageField(upload_to="room_photos",
                               processors=[ResizeToFill(1024, 1024)],
                               options={'quality': 60})
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):
    """ Room Model Definition """

    name = models.CharField(_("name"), max_length=25)  # 이름
    description = models.TextField(_("description"), )  # 설명
    country = CountryField(_("country"), )  # 나라
    city = models.CharField(_("city"), max_length=20)  # 도시
    price = models.IntegerField(_("price"), )  # 가격
    address = models.CharField(_("address"), max_length=30)  # 주소
    guests = models.IntegerField(_("guests"), )  # 게스트
    beds = models.IntegerField(_("beds"), )  # 침대
    bedrooms = models.IntegerField(_("bedrooms"), )  # 침실
    baths = models.IntegerField(_("baths"), )  # 화장실
    check_in = models.TimeField(_("check_in"), )
    check_out = models.TimeField(_("check_out"), )
    instant_book = models.BooleanField(_("instant_book"), default=False)
    host = models.ForeignKey("users.User", related_name="rooms", on_delete=models.CASCADE)
    room_type = models.ForeignKey("RoomType", related_name="rooms", on_delete=models.CASCADE)
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_rating = 0
        for review in all_reviews:
            all_rating += review.rating_average()
        if all_rating == 0:
            return 0
        else:
            length = len(all_reviews)
            return round(all_rating / length, 2)

    def first_photo(self):
        try:
            photo, = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        try:
            photos = self.photos.all()[1:5]
        except ValueError:
            return None
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = now.month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]

    class Meta:
        ordering = ('name',)


