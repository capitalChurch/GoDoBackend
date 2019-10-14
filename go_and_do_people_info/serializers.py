from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User

from go_and_do_people_info.models import (Country, Event, Ministry, News,
                                          Prayer, Ticket, UserProfile,
                                          Volunteer)
from phonenumber_field import serializerfields
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','first_name', 'last_name')
        read_only_fields = ('email',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'url',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'groups',
        ]

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'url',
            'user',
            'date_of_birth',
            'gender',
            'phone_number',
            'mobile_number',
            'zip_code',
            'street',
            'district',
            'city',
            'state',
            'date_joined',
            'avatar',
        ]
class MinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministry
        fields = ['url', 'name', 'info']
    
class VolunteerSerializer(serializers.HyperlinkedModelSerializer):
    member = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False, help_text='Field documentation!')
    ministry = serializers.PrimaryKeyRelatedField(queryset=Ministry.objects.all(), many=False, read_only=False, help_text='Field documentation!')
    class Meta:
        model = Volunteer
        fields = ['url', 'member', 'ministry', 'is_leader']
        validators = [
            UniqueTogetherValidator(
                queryset=Volunteer.objects.all(),
                fields=['member', 'ministry']
            )
        ]
    
class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ['url', 'name']


class PrayerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False, help_text='Field documentation!')
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), many=False, read_only=False, help_text='Field documentation!')
    class Meta:
        model = Prayer
        fields = ['url', 'timestamp', 'user', 'country']
        validators = [
            UniqueTogetherValidator(
                queryset=Prayer.objects.all(),
                fields=['timestamp', 'user', 'country']
            )
        ]

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False, help_text='Field documentation!')
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), many=False, read_only=False, help_text='Field documentation!')
    class Meta:
        model = News
        fields = ['url', 'title', 'text', 'timestamp', 'author', 'country']
        validators = [
            UniqueTogetherValidator(
                queryset=News.objects.all(),
                fields=['title', 'text', 'timestamp', 'author', 'country']
            )
        ]

class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['url', 'name', 'datetime', 'description', 'venue']

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False, help_text='Field documentation!')
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), many=False, read_only=False, help_text='Field documentation!')
    class Meta:
        model = Ticket
        fields = ['url', 'title', 'user', 'event', 'ticket_id', 'purchase_date', 'modified', 'price']
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=['title', 'event', 'ticket_id']
            )
        ]
