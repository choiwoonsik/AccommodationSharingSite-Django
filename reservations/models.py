import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models
from django.utils.translation import gettext_lazy as _


class BookedDay(core_models.TimeStampedModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Booked Day")
        verbose_name_plural = _("Booked Days")

    def __str__(self):
        return str(self.day)


class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, _("Pending")),
        (STATUS_CONFIRMED, _("Confirmed")),
        (STATUS_CANCELED, _("Canceled")),
    )

    status = models.CharField(_("status"), max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE, null=True
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE, null=True
    )
    check_in = models.DateField(_("check_in"), null=True, blank=True)
    check_out = models.DateField(_("check_out"), null=True, blank=True)

    def __str__(self):
        return f"{self.room} : {self.check_in} - {self.check_out}"

    def in_progress(self):
        now = timezone.now().date()
        return self.check_in <= now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True

    def save(self, *args, **kwargs):

        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects\
                .filter(day__range=(start, end))\
                .filter(reservation__room__pk=self.room.pk)\
                .exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)
