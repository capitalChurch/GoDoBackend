import re, datetime, uuid

from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
          raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                 is_staff=is_staff, is_active=True,
                 is_superuser=is_superuser, last_login=now,
                 date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True,
                 **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. \
                    Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_trusty = models.BooleanField(_('trusty'), default=False,
        help_text=_('Designates whether this user has confirmed his account.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=datetime.date.today)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_subscribed = models.BooleanField(_('subscribed'), default=True)
    phone_number = PhoneNumberField(blank=False, null=True)
    mobile_number = PhoneNumberField(blank=False)
    zip_code = models.CharField(_('zip code'), max_length=9, null=True)
    street = models.CharField(_('street name'), max_length=100, null=True)
    district = models.CharField(_('district name'), max_length=100, null=True)
    city = models.CharField(_('city'), max_length=100, null=True)
    state = models.CharField(_('state'), max_length=100, null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    REQUIRED_FIELDS = [
            'user',
            'date_of_birth',
            'gender',
            'mobile_number',
            ]
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('users profiles')
        # ordering = ('user', )

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


class Ministry(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True, blank=False)
    info = models.CharField(_('info'), max_length=255, blank=True)
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Volunteer(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
    is_leader = models.BooleanField(_('leader'), default=False)
    def __unicode__(self):
        return self.member.name + " " + self.ministry.name

class Country(models.Model):
    name = models.CharField(_('country name'), max_length=30, unique=True)
    REQUIRED_FIELDS = [
        'name'
    ]

class Prayer(models.Model):
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

class News(models.Model):
    title = models.CharField(_('title name'), max_length=100, unique=True)
    text = models.TextField(_('text'), max_length=1000)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    REQUIRED_FIELDS = [
        'title',
        'text',
        'author',
        'country'
    ]

class Event(models.Model):
    name = models.CharField(_('event name'), max_length=100, unique=True)
    datetime = models.DateTimeField(_('datetime'))
    description = models.TextField(_('description'), max_length=200)
    venue = models.CharField(_('event venue'), max_length=100, unique=False)
    REQUIRED_FIELDS = [
        'name',
        'datetime',
        'description',
        'venue'
    ]

class Ticket(models.Model):
    title = models.CharField(_('title'), max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_id = models.CharField(_('ticket number'), max_length=255, blank=True)
    purchase_date = models.DateTimeField(_('purchase date'), auto_now=True)
    modified = models.DateTimeField(_('modified'), auto_now_add=True)
    price = models.FloatField(_('title name'), null=False, default=0)

    def save(self, *args, **kwargs):
        if len(self.ticket_id.strip(" "))==0:
            self.ticket_id = str(uuid.uuid4()).split("-")[-1]

        super(Ticket, self).save(*args, **kwargs)