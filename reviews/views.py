from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from . import forms
from django.utils.translation import gettext_lazy as _
from rooms import models as room_models


def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, _("Room reviewed"))
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

