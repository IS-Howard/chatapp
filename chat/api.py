from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from chat.serializers import UserModelSerializer, ChatRoomNameSerializer, ChatRoomUserSerializer
from chat.models import ChatRoom, ChatRoomMembership


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)
    
class ChatRoomModelViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomNameSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all Room

    def list(self, request, *args, **kwargs):
        return super(ChatRoomModelViewSet, self).list(request, *args, **kwargs)
    
class ChatRoomUserModelViewSet(ModelViewSet):
    queryset = ChatRoomMembership.objects.all()
    serializer_class = ChatRoomUserSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all Room

    def list(self, request, *args, **kwargs):
        room_name = request.query_params.get('room_name', None)

        # Filter the queryset to get usernames from ChatRoomMembership for the current chat room
        self.queryset = ChatRoomMembership.objects.filter(chat_room=room_name)
        self.queryset = self.queryset.exclude(user=request.user)
        return super(ChatRoomUserModelViewSet, self).list(request, *args, **kwargs)