from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from go_and_do_people_info.models import (Country, Event, Ministry, News,
                                          Prayer, Ticket, UserProfile,
                                          Volunteer)
from go_and_do_people_info.serializers import (MinistrySerializer,
                                               UserProfileSerializer,
                                               UserSerializer,
                                               VolunteerSerializer,
                                               CountrySerializer,
                                               PrayerSerializer,
                                               NewsSerializer,
                                               EventSerializer,
                                               TicketSerializer)
from rest_auth.registration.views import RegisterView
from rest_framework import viewsets
from rest_framework_swagger.views import get_swagger_view

User = get_user_model()

class CustomRegisterView(RegisterView):
    queryset = User.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MinistryViewSet(viewsets.ModelViewSet):
    queryset = Ministry.objects.all()
    serializer_class = MinistrySerializer

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class PrayerViewSet(viewsets.ModelViewSet):
    queryset = Prayer.objects.all()
    serializer_class = PrayerSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer