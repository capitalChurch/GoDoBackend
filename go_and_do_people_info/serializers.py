from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import serializers
from go_and_do_people_info.models import UserProfile, Ministry, MinistryMember
from phonenumber_field import serializerfields
from rest_auth.registration.serializers import RegisterSerializer
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

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

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
    
class MinistryMemberSerializer(serializers.HyperlinkedModelSerializer):
    # members = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    member = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False)
    ministry = serializers.PrimaryKeyRelatedField(queryset=Ministry.objects.all(), many=False, read_only=False)
    class Meta:
        model = MinistryMember
        fields = ['url', 'member', 'ministry', 'is_leader']
        validators = [
            UniqueTogetherValidator(
                queryset=MinistryMember.objects.all(),
                fields=['member', 'ministry']
            )
        ]
    
    # def save()

