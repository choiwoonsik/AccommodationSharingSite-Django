from django import template
from users import models as user_models
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    if user.pk is None:
        return False
    the_list = list_models.List.objects.get_or_none(user=user, name="My Favorites Houses")
    if the_list is not None:
        return room in the_list.rooms.all()
    else:
        return False
