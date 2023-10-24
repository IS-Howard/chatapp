from django.urls import path

from . import views
from accounts.views import custom_logout
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", login_required(views.index), name="index"),
    path('logout/', custom_logout, name="logout"),
    path("<str:room_name>/", login_required(views.room), name="room"),
]