from django.shortcuts import render, redirect, reverse
from users import models as user_models
from django.http import Http404
from django.views.generic import DetailView, View
from . import models, forms


def go_conversations(request, r_pk, a_pk, b_pk):
    try:
        user_a = user_models.User.objects.get(pk=a_pk)
    except user_models.User.DoesNotExist:
        user_a = None
    try:
        user_b = user_models.User.objects.get(pk=b_pk)
    except user_models.User.DoesNotExist:
        user_b = None
    if user_a is not None and user_b is not None:
        conversation = models.Conversation.objects.filter(
            participants=user_a
        ).filter(
            participants=user_b
        )
        if conversation.count() == 0:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_a, user_b)
            conversation = models.Conversation.objects.filter(
                participants=user_a
            ).filter(
                participants=user_b
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation[0].pk, "r_pk": r_pk}))
    else:
        raise Http404()


class ConversationsDetailView(View):

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        r_pk = kwargs.get('r_pk')
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation, "r_pk": r_pk},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get('message', None)
        pk = kwargs.get('pk')
        r_pk = kwargs.get('r_pk')
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if message is not None:
            models.Message.objects.create(
                message=message,
                user=self.request.user,
                conversation=conversation
            )
            return redirect(reverse("conversations:detail", kwargs={"pk": pk, "r_pk": r_pk}))

