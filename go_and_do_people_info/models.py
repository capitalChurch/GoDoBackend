from django.db import models

from django.core import validators
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
import re

from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField

class Ministry(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True, blank=False)
    info = models.CharField(_('info'), max_length=255, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    username = models.CharField(
        _('username'),
        max_length=30,
        blank=False,
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _('Enter a valid username.'),
                _('invalid')
            )
        ]
    )
    first_name = models.CharField(_('first name'), max_length=100, blank=False)
    last_name = models.CharField(_('last name'), max_length=100, blank=False)
    email = models.EmailField(_('email address'), unique=True)
    birth_date = models.DateTimeField(_('birth date'), blank=False)
    phone_number = PhoneNumberField(blank=False)
    address = AddressField(on_delete=models.CASCADE, blank=False)
    subscribed = models.BooleanField(_('subscribed'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    ministry = models.ManyToManyField(Ministry)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'email', 'birth_date', 'phone_number', 'address'
    ]

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('users profiles')
        ordering = ('first_name', 'last_name', )

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