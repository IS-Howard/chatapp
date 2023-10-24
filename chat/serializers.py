from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from chat.models import ChatRoom, ChatRoomMembership
from rest_framework.serializers import ModelSerializer, SerializerMethodField

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class ChatRoomUserSerializer(ModelSerializer):
    user = SerializerMethodField()

    class Meta:
        model = ChatRoomMembership
        fields = ('user',)

    def get_user(self, obj):
        return obj.user.username
    
class ChatRoomNameSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ('name',)

