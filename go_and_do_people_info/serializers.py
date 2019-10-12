from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import serializers
from go_and_do_people_info.models import Ministry, UserProfile, Address
from phonenumber_field import serializerfields
from rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
        }

class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','name','date_of_birth')
        read_only_fields = ('email',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['url', 'username', 'email', 'groups', 'first_name', 'last_name', 'date_of_birth', 'gender']


class MinistrySerializer(serializers.HyperlinkedModelSerializer):
    users = UserSerializer(many=True)
    class Meta:
        model = User
        fields = ['url', 'name', 'info', 'users']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    zip_code = serializers.CharField(required=True, allow_blank=False, max_length=9)
    street = serializers.CharField(required=True, allow_blank=False, max_length=100)
    district = serializers.CharField(required=True, allow_blank=False, max_length=100)
    city = serializers.CharField(required=True, allow_blank=False, max_length=100)
    state = serializers.CharField(required=True, allow_blank=False, max_length=100)
    class Meta:
        model = Address
        fields = ['url', 'zip_code', 'street', 'district', 'city', 'state', 'user']

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'url',
            'user',
            # 'phone_number',
            'address',
            # 'subscribed',
            # 'date_joined',
            # 'is_active',
            'is_staff',
            # 'is_member',
            # 'member_since',
            # 'baptism_date',
            # 'ministries',
            # 'avatar'
        ]
    
    user = UserSerializer(required=True)
    # first_name = serializers.CharField(required=True, allow_blank=False)
    # last_name = serializers.CharField(required=True, allow_blank=False)
    # birth_date = serializers.DateTimeField(required=True)
    # phone_number = serializerfields.PhoneNumberField(required=True)
    address = AddressSerializer(required=True)
    # subscribed = serializers.BooleanField(required=False)
    # date_joined = serializers.DateTimeField(required=False)
    # is_active = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    # is_member = serializers.BooleanField(required=False)
    # member_since = serializers.DateTimeField(required=False)
    # baptism_date = serializers.DateTimeField(required=False)
    # ministries = MinistrySerializer(required=False)
    # avatar = serializers.ImageField(required=False)

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return UserProfile.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance