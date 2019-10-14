from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from go_and_do_people_info.models import Ministry, MinistryMember, UserProfile
from go_and_do_people_info.serializers import (MinistryMemberSerializer,
                                               MinistrySerializer,
                                               UserProfileSerializer,
                                               UserSerializer)
from rest_auth.registration.views import RegisterView
from rest_framework import viewsets

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

class MinistryMemberViewSet(viewsets.ModelViewSet):
    queryset = MinistryMember.objects.all()
    serializer_class = MinistryMemberSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

