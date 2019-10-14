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
    retrieve:
        Return a user instance.

    list:
        Return all users, ordered by most recently joined.

    create:
        Create a new user.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    update:
        Update a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MinistryViewSet(viewsets.ModelViewSet):
    """
    General API documentation (not wisible in the swagger view)

    get:
    GET-specific documentation!

    Lorem ipsum

    post:
    POST-specific documentation!

    Dolor **sit amet**
    """
    queryset = Ministry.objects.all()
    serializer_class = MinistrySerializer

class VolunteerViewSet(viewsets.ModelViewSet):
    """
    General API documentation (not wisible in the swagger view)

    get:
    GET-specific documentation!

    Lorem ipsum

    post:
    POST-specific documentation!

    Dolor **sit amet**
    """
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    General API documentation (not wisible in the swagger view)

    get:
    GET-specific documentation!

    Lorem ipsum

    post:
    POST-specific documentation!

    Dolor **sit amet**
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CountryViewSet(viewsets.ModelViewSet):
    """
    General API documentation (not wisible in the swagger view)

    get:
    GET-specific documentation!

    Lorem ipsum

    post:
    POST-specific documentation!

    Dolor **sit amet**
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class PrayerViewSet(viewsets.ModelViewSet):
    """
    General API documentation (not wisible in the swagger view)

    get:
    GET-specific documentation!

    Lorem ipsum

    post:
    POST-specific documentation!

    Dolor **sit amet**
    """
    queryset = Prayer.objects.all()
    serializer_class = PrayerSerializer

class NewsViewSet(viewsets.ModelViewSet):
    """
    General API documentation (not wisible in the swagger view)

    get:
    GET-specific documentation!

    Lorem ipsum

    post:
    POST-specific documentation!

    Dolor **sit amet**
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    General API documentation (not wisible in the swagger view)

    get:
    GET-specific documentation!

    Lorem ipsum

    post:
    POST-specific documentation!

    Dolor **sit amet**
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TicketViewSet(viewsets.ModelViewSet):
    """
    General API documentation (not wisible in the swagger view)

    get:
    GET-specific documentation!

    Lorem ipsum

    post:
    POST-specific documentation!

    Dolor **sit amet**
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer