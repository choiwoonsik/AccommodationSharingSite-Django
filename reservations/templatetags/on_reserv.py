from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_reserv(context, room):
    user = context.request.user
    the_reserv = reservation_models.Reservation.objects.filter(guest=user, room=room)
    if the_reserv.count() > 0:
        return the_reserv[0]
    return the_reserv
