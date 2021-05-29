from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    ONE = 1
    TWO = 2
    THR = 3
    FOR = 4
    FIV = 5

    RATING_CHOICE = (
        (ONE, "1"),
        (TWO, "2"),
        (THR, "3"),
        (FOR, "4"),
        (FIV, "5"),
    )

    # 평가 항목
    # accuracy = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(_("review"))
    accuracy = models.IntegerField(_("accuracy"), choices=RATING_CHOICE, default=ONE)
    communication = models.IntegerField(_("communication"), choices=RATING_CHOICE, default=ONE)
    cleanliness = models.IntegerField(_("cleanliness"), choices=RATING_CHOICE, default=ONE)
    location = models.IntegerField(_("location"), choices=RATING_CHOICE, default=ONE)
    check_in = models.IntegerField(_("check_in"), choices=RATING_CHOICE, default=ONE)
    value = models.IntegerField(_("value"), choices=RATING_CHOICE, default=ONE)
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

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

    rating_average.short_description = "average"

    class Meta:
        ordering = ('-created',)
