from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from go_and_do_people_info.models import Address, Ministry, UserProfile
from go_and_do_people_info.serializers import (AddressSerializer,
                                               GroupSerializer,
                                               MinistrySerializer,
                                               UserProfileSerializer,
                                               UserSerializer)
from rest_framework import viewsets
from rest_auth.registration.views import RegisterView

User = get_user_model()

class CustomRegisterView(RegisterView):
    queryset = User.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class MinistryViewSet(viewsets.ModelViewSet):
    queryset = Ministry.objects.all()
    serializer_class = MinistrySerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
