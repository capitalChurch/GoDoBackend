import re
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class Address(models.Model):
    zip_code = models.CharField(_('zip code'), max_length=9)
    street = models.CharField(_('street name'), max_length=100)
    district = models.CharField(_('district name'), max_length=100)
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state'), max_length=100)

class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, name, date_of_birth, password=None):
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,         
            name=name,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            name= "True",
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    username = None
    name = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=100, blank=False)
    last_name = models.CharField(_('last name'), max_length=100, blank=False)
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(default=datetime.date.today)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'first_name', 'last_name', 'gender']
    objects = UserManager()

    def __str__(self):
        return "{}".format(self.email)

class Ministry(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True, blank=False)
    info = models.CharField(_('info'), max_length=255, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    address = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='user')
    # phone_number = PhoneNumberField(blank=False)
    # mobile_number = PhoneNumberField(blank=False)
    # subscribed = models.BooleanField(_('subscribed'), default=True)
    # date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_member = models.BooleanField(_('member'), default=False)
    # member_since = models.DateTimeField(_('date member'), auto_now_add=False)
    # baptism_date = models.DateTimeField(_('date baptism'), auto_now_add=False)
    member_of = models.ManyToManyField(Ministry, related_name='user_in_ministry', through='MinistryMember')
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    REQUIRED_FIELDS = ['user']
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('users profiles')
        ordering = ('user', )

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

class MinistryMember(models.Model):
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
    role = models.CharField(max_length=40)
    def __unicode__(self):
        return self.member.name + " " + self.ministry.name + " - " + self.role