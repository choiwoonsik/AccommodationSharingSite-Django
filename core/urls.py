from django.urls import path
from rooms import views as room_views
from . import views

app_name = "core"

urlpatterns = [path("", room_views.HomeView.as_view(), name="home"),
               path("copyrights/", views.index, name="copyrights"),
               ]
