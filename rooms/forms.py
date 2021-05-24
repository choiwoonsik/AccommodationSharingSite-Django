from django import forms
from . import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class SearchForm(forms.Form):

    city = forms.CharField(initial=_("Anywhere"))
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label=_("Any kind"), queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(
        required=False, widget=forms.NumberInput(attrs={"placeholder": _("Max Price ($)")})
    )


class CreatePhotoForm(forms.ModelForm):

    class Meta:
        model = models.Photo
        fields = (
            _("caption"),
            _("file"),
        )

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
