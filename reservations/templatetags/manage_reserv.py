from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag(takes_context=True)
def manage_reserv(context, room):
    user = context.request.user
    the_reserv = reservation_models.Reservation.objects.filter(room__host=user).filter(room=room)
    if the_reserv.count() > 0:
        return the_reserv
    return None
