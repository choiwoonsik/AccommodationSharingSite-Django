from django.urls import path
from . import views


app_name = "conversations"

urlpatterns = (
    path("go/<int:r_pk>/<int:a_pk>/<int:b_pk>", views.go_conversations, name="go"),
    path("<int:pk>/<int:r_pk>", views.ConversationsDetailView.as_view(), name="detail"),
)
