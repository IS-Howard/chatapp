from django.urls import path, include
from . import views
from accounts.views import custom_logout
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter

from chat.api import UserModelViewSet, ChatRoomModelViewSet, ChatRoomUserModelViewSet, MessageModelViewSet

router = DefaultRouter()
router.register(r'user', UserModelViewSet, basename='user-api')
router.register(r'room', ChatRoomModelViewSet, basename='room-api')
router.register(r'roomuser', ChatRoomUserModelViewSet, basename='roomuser-api')
router.register(r'message', MessageModelViewSet, basename='message-api')

urlpatterns = [
    path("", login_required(views.index), name="index"),
    path('logout/', custom_logout, name="logout"),
    path("<str:room_name>/", login_required(views.room), name="room"),
    path(r'api/v1/', include(router.urls)),
]