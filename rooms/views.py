from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.utils import timezone
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from . import models
from users import mixins as user_mixins


class HomeView(ListView):
    """ HomeView Definition """

    model = models.Room
    paginate_by = 8
    ordering = "name"
    paginate_orphans = 4
    page_kwarg = "page"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


# @login_required()
class RoomDetail(DetailView):
    """ RoomDetail Definition """

    model = models.Room


class SearchView(View):

    def get(self, request):
        city = request.GET.get("city")

        if city:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")

                filter_args = {}

                if city != "Anywhere" and city != "제한없음":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if price is not None:
                    filter_args["price__lte"] = price

                if room_type is not None:
                    filter_args["room_type"] = room_type

                rooms = models.Room.objects.filter(**filter_args)

                qs = rooms.order_by("-created")

                paginator = Paginator(qs, 10, 5)

                page = request.GET.get("page", 1)

                if rooms.count() == 0:
                    rooms = None
                else:
                    rooms = paginator.get_page(page)

                return render(
                    request,
                    "rooms/search.html",
                    {
                        "form": form,
                        "rooms": rooms,
                    },
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html",
                      {
                          "form": form,
                          "rooms": None,
                      })


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = 'rooms/room_edit.html'
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

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, RoomDetail):
    model = models.Room
    template_name = 'rooms/room_photos.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, _("Can't delete that photo"))
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, _("Photo Deleted"))
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_message = _("Photo Updated")

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, FormView):
    model = models.Photo
    template_name = "rooms/photo_create.html"
    fields = (
        _("caption"),
        _("file"),
    )
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        form.save(pk)
        messages.success(self.request, _("Photo Uploaded"))
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):
    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(self.request, _("Room Created"))
        return redirect(reverse("rooms:detail", kwargs={'pk': room.pk}))
