from django.contrib.auth.models import User, Group
from rest_framework import serializers
from go_and_do_people_info.models import Ministry, UserProfile

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'email', 'first_name', 'last_name']

class MinistrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ['url', 'name', 'info']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']